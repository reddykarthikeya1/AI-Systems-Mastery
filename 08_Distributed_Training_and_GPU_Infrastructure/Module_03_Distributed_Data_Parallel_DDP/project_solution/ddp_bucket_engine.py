"""Production reference implementation for DDP Gradient Bucket Engine."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bucket:
    bucket_id: int
    params: list[str]
    capacity_bytes: int
    total_bytes: int = 0
    pending_params: set[str] = None

    def __post_init__(self) -> None:
        if self.pending_params is None:
            self.pending_params = set()


class DDPBucketManager:
    """Manages gradient bucketing and overlapping communication with backward pass."""

    def __init__(self, bucket_size_mb: float = 25.0) -> None:
        self.bucket_capacity_bytes = int(bucket_size_mb * 1024 * 1024)
        self.buckets: list[Bucket] = []
        self.param_to_bucket: dict[str, int] = {}
        self.triggered_buckets: set[int] = set()

    def register_parameter(self, name: str, size_bytes: int) -> int:
        """Register parameter into bucket in reverse topological order."""
        if not self.buckets or (self.buckets[-1].total_bytes + size_bytes > self.bucket_capacity_bytes):
            new_id = len(self.buckets)
            b = Bucket(bucket_id=new_id, params=[name], capacity_bytes=self.bucket_capacity_bytes, total_bytes=size_bytes)
            b.pending_params.add(name)
            self.buckets.append(b)
            self.param_to_bucket[name] = new_id
            return new_id

        curr_b = self.buckets[-1]
        curr_b.params.append(name)
        curr_b.pending_params.add(name)
        curr_b.total_bytes += size_bytes
        self.param_to_bucket[name] = curr_b.bucket_id
        return curr_b.bucket_id

    def mark_param_ready(self, name: str) -> bool:
        """Mark parameter gradient ready; returns True if bucket triggered AllReduce."""
        b_id = self.param_to_bucket[name]
        bucket = self.buckets[b_id]
        bucket.pending_params.remove(name)

        if len(bucket.pending_params) == 0 and b_id not in self.triggered_buckets:
            self.triggered_buckets.add(b_id)
            return True
        return False


def simulate_ddp_overlap(
    param_sizes_bytes: list[int],
    compute_times_ms: list[float],
    bucket_size_mb: float = 25.0,
    bandwidth_gbs: float = 50.0,
) -> dict[str, float]:
    """Simulate execution time and overlap savings of DDP bucketing.

    Compares:
    - Serial time: Sum(compute) + AllReduce(Total bytes)
    - Overlapped time: Buckets launched as they fill during backprop.
    """
    total_compute_ms = sum(compute_times_ms)
    total_bytes = sum(param_sizes_bytes)

    # 2 * (N-1)/N * S / BW
    total_comm_ms = (2.0 * total_bytes / (bandwidth_gbs * 1e9)) * 1e3
    serial_time_ms = total_compute_ms + total_comm_ms

    # Simulate bucketing
    mgr = DDPBucketManager(bucket_size_mb=bucket_size_mb)
    for idx, (sz, _) in enumerate(zip(param_sizes_bytes, compute_times_ms)):
        mgr.register_parameter(f"param_{idx}", sz)

    curr_time_ms = 0.0
    network_free_time_ms = 0.0

    for idx, (_, comp_t) in enumerate(zip(param_sizes_bytes, compute_times_ms)):
        curr_time_ms += comp_t
        if mgr.mark_param_ready(f"param_{idx}"):
            b_id = mgr.param_to_bucket[f"param_{idx}"]
            b_bytes = mgr.buckets[b_id].total_bytes
            b_comm_ms = (2.0 * b_bytes / (bandwidth_gbs * 1e9)) * 1e3
            start_comm = max(curr_time_ms, network_free_time_ms)
            network_free_time_ms = start_comm + b_comm_ms

    overlapped_time_ms = max(curr_time_ms, network_free_time_ms)
    speedup = serial_time_ms / overlapped_time_ms if overlapped_time_ms > 0 else 1.0

    return {
        "serial_time_ms": serial_time_ms,
        "overlapped_time_ms": overlapped_time_ms,
        "speedup_factor": speedup,
        "overlap_percentage": max(0.0, (serial_time_ms - overlapped_time_ms) / total_comm_ms * 100.0) if total_comm_ms > 0 else 100.0,
    }
