"""Starter template for DDP Gradient Bucket Engine."""
from __future__ import annotations


class DDPBucketManager:
    """Manages gradient bucketing and overlapping communication with backward pass."""

    def __init__(self, bucket_size_mb: float = 25.0) -> None:
        raise NotImplementedError("Implement DDPBucketManager.__init__")

    def register_parameter(self, name: str, size_bytes: int) -> int:
        """Register parameter into bucket in reverse topological order."""
        raise NotImplementedError("Implement DDPBucketManager.register_parameter")

    def mark_param_ready(self, name: str) -> bool:
        """Mark parameter gradient ready; returns True if bucket triggered AllReduce."""
        raise NotImplementedError("Implement DDPBucketManager.mark_param_ready")


def simulate_ddp_overlap(
    param_sizes_bytes: list[int],
    compute_times_ms: list[float],
    bucket_size_mb: float = 25.0,
    bandwidth_gbs: float = 50.0,
) -> dict[str, float]:
    """Simulate execution time and overlap savings of DDP bucketing."""
    raise NotImplementedError("Implement simulate_ddp_overlap")
