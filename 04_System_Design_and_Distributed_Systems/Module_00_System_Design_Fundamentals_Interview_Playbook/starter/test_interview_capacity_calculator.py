"""Tests for Module 00: Interview Capacity Estimation Calculator."""

import pytest
from interview_capacity_calculator import CapacityCalculator, SystemCapacityProfile


@pytest.fixture
def twitter_profile() -> SystemCapacityProfile:
    """Sample profile representing Twitter-like scale:
    500M DAU, 20 reads/day, 2 writes/day, 200B text payload.
    """
    return SystemCapacityProfile(
        dau=500_000_000,
        reads_per_user_day=20.0,
        writes_per_user_day=2.0,
        read_payload_bytes=2_000,  # 2 KB timeline response
        write_payload_bytes=250,   # 250 B tweet metadata
        peak_multiplier=2.5,
        storage_years=5,
        cache_read_ratio=0.20,
    )


def test_qps_calculation(twitter_profile: SystemCapacityProfile) -> None:
    qps = CapacityCalculator.calculate_qps(twitter_profile)
    # Writes: 500M * 2 = 1B / 86400 = ~11,574.07 QPS
    assert qps["avg_write_qps"] == 11574.07
    assert qps["peak_write_qps"] == 28935.19
    # Reads: 500M * 20 = 10B / 86400 = ~115,740.74 QPS
    assert qps["avg_read_qps"] == 115740.74
    assert qps["peak_read_qps"] == 289351.85


def test_bandwidth_calculation(twitter_profile: SystemCapacityProfile) -> None:
    bw = CapacityCalculator.calculate_bandwidth(twitter_profile)
    # Ingress: 11,574.07 * 250 B = ~2.89 MB/s = ~23.15 Mbps
    assert bw["ingress_mb_per_sec"] == 2.89
    assert bw["ingress_mbps"] == 23.15
    # Egress: 115,740.74 * 2000 B = ~231.48 MB/s = ~1851.85 Mbps
    assert bw["egress_mb_per_sec"] == 231.48
    assert bw["egress_mbps"] == 1851.85


def test_storage_calculation(twitter_profile: SystemCapacityProfile) -> None:
    storage = CapacityCalculator.calculate_storage(twitter_profile)
    # Daily writes: 1B * 250 B = 250 GB/day
    assert storage["daily_storage_gb"] == 250.0
    # Annual: 250 GB * 365 = 91.25 TB/year
    assert storage["annual_storage_tb"] == 91.25
    # 5-Year: 91.25 * 5 = 456.25 TB
    assert storage["multi_year_storage_tb"] == 456.25


def test_cache_size_calculation(twitter_profile: SystemCapacityProfile) -> None:
    cache = CapacityCalculator.calculate_cache_size(twitter_profile)
    # Daily read volume: 10B * 2 KB = 20,000 GB = 20 TB
    assert cache["daily_read_volume_gb"] == 20000.0
    # 20% cache = 4,000 GB RAM
    assert cache["ram_cache_required_gb"] == 4000.0


def test_profile_validation_rejects_negative_or_zero_values() -> None:
    with pytest.raises(ValueError, match="DAU must be strictly positive"):
        SystemCapacityProfile(
            dau=0,
            reads_per_user_day=10,
            writes_per_user_day=1,
            read_payload_bytes=100,
            write_payload_bytes=100,
        )

    with pytest.raises(ValueError, match="Requests per user cannot be negative"):
        SystemCapacityProfile(
            dau=1000,
            reads_per_user_day=-1.0,
            writes_per_user_day=1,
            read_payload_bytes=100,
            write_payload_bytes=100,
        )
