"""Unit tests for Module 01 Capacity Estimator & Sizing Engine."""

import pytest
from capacity_estimator import CapacityEstimator


@pytest.fixture
def standard_planner() -> CapacityEstimator:
    # 100M DAU, 10 reads, 1 write per user/day
    # Read size 2KB, Write size 500 bytes
    return CapacityEstimator(
        dau=100_000_000,
        read_ops_per_user_day=10,
        write_ops_per_user_day=1,
        avg_read_payload_bytes=2_000,
        avg_write_payload_bytes=500,
        peak_multiplier=2.0,
        retention_years=5,
        replication_factor=3,
        cache_coverage_ratio=0.20,
    )


def test_invalid_parameters_raise_value_error() -> None:
    with pytest.raises(ValueError, match="DAU must be greater than zero"):
        CapacityEstimator(dau=0, read_ops_per_user_day=1, write_ops_per_user_day=1,
                          avg_read_payload_bytes=10, avg_write_payload_bytes=10)

    with pytest.raises(ValueError, match="Operations per user cannot be negative"):
        CapacityEstimator(dau=100, read_ops_per_user_day=-1, write_ops_per_user_day=1,
                          avg_read_payload_bytes=10, avg_write_payload_bytes=10)

    with pytest.raises(ValueError, match="Payload sizes must be positive integers"):
        CapacityEstimator(dau=100, read_ops_per_user_day=1, write_ops_per_user_day=1,
                          avg_read_payload_bytes=0, avg_write_payload_bytes=10)


def test_qps_estimation_math(standard_planner: CapacityEstimator) -> None:
    qps = standard_planner.estimate_qps()

    # 100M * 10 reads / 86400 = 11,574.07
    assert pytest.approx(qps.avg_read_qps, 0.1) == 11574.07
    # 100M * 1 write / 86400 = 1,157.41
    assert pytest.approx(qps.avg_write_qps, 0.1) == 1157.41
    # Total QPS = 12,731.48
    assert pytest.approx(qps.avg_total_qps, 0.1) == 12731.48
    # Peak QPS = 2x
    assert pytest.approx(qps.peak_total_qps, 0.1) == 25462.96


def test_bandwidth_estimation_math(standard_planner: CapacityEstimator) -> None:
    bw = standard_planner.estimate_bandwidth()

    # Peak write QPS = 2,314.82 * 500 bytes = ~1.16 MB/s -> ~9.26 Mbps
    assert bw.ingress_mb_per_sec > 1.0
    assert bw.ingress_mbps > 8.0

    # Peak read QPS = 23,148.14 * 2,000 bytes = ~46.30 MB/s -> ~370.37 Mbps
    assert bw.egress_mb_per_sec > 40.0
    assert bw.egress_mbps > 320.0


def test_storage_growth_and_replication(standard_planner: CapacityEstimator) -> None:
    storage = standard_planner.estimate_storage()

    # Daily writes: 100M * 500 bytes = 50 GB/day raw
    assert pytest.approx(storage.daily_raw_storage_gb, 0.1) == 50.0
    # Replicated 3x = 150 GB/day
    assert pytest.approx(storage.daily_replicated_storage_gb, 0.1) == 150.0

    # 5 Years = 50 GB * 1825 days / 1000 = 91.25 TB raw
    assert pytest.approx(storage.total_raw_storage_tb, 0.1) == 91.25
    assert pytest.approx(storage.total_replicated_storage_tb, 0.1) == 273.75


def test_cache_ram_sizing_and_node_allocation(standard_planner: CapacityEstimator) -> None:
    cache = standard_planner.estimate_cache()

    # Daily reads: 100M * 10 * 2KB = 2,000 GB/day read volume
    assert pytest.approx(cache.daily_read_volume_gb, 0.1) == 2000.0
    # 20% cache coverage = 400 GB RAM
    assert pytest.approx(cache.recommended_cache_ram_gb, 0.1) == 400.0
    # 400GB / 48GB usable per node = ceil(8.33) = 9 nodes
    assert cache.nodes_required_64gb_ram == 9
