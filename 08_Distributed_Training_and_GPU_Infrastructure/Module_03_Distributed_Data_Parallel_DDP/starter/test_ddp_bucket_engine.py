"""Unit tests for DDP Gradient Bucket Engine."""
from __future__ import annotations

from ddp_bucket_engine import (
    DDPBucketManager,
    simulate_ddp_overlap,
)


def test_ddp_bucket_manager_triggering() -> None:
    # 10MB bucket size
    mgr = DDPBucketManager(bucket_size_mb=10.0)

    # Register three 4MB parameters -> fit into 1 bucket (12MB triggers new bucket)
    mgr.register_parameter("p1", 4 * 1024 * 1024)
    mgr.register_parameter("p2", 4 * 1024 * 1024)
    mgr.register_parameter("p3", 4 * 1024 * 1024)

    # p1 and p2 in bucket 0, p3 in bucket 1
    assert mgr.param_to_bucket["p1"] == 0
    assert mgr.param_to_bucket["p2"] == 0
    assert mgr.param_to_bucket["p3"] == 1

    # Mark p1 ready -> bucket 0 not ready yet (p2 pending)
    assert mgr.mark_param_ready("p1") is False

    # Mark p2 ready -> bucket 0 complete! Triggers AllReduce!
    assert mgr.mark_param_ready("p2") is True


def test_ddp_overlap_simulation() -> None:
    # 5 layers, each 20MB, compute time 10ms
    sizes = [20 * 1024 * 1024] * 5
    times = [10.0] * 5

    res = simulate_ddp_overlap(sizes, times, bucket_size_mb=25.0, bandwidth_gbs=50.0)

    assert res["serial_time_ms"] > res["overlapped_time_ms"]
    assert res["speedup_factor"] > 1.0
    assert res["overlap_percentage"] > 0.0
