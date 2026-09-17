"""Problem 01 — Bucket Gradient Allreduce

Topic: 03 Distributed Data Parallel DDP
Target: Production-grade implementation

Partition parameter gradients into fixed-capacity buckets for overlapping AllReduce.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bucket_gradient_allreduce(param_sizes_mb: list[float], bucket_cap_mb: float = 25.0) -> list[list[int]]:
    """Group parameter indices (0..len-1) into buckets of capacity at most bucket_cap_mb.
    Indices are added in reverse order (backward pass executes from last layer to first).
    Returns list of bucket lists containing parameter indices.
    """
    raise NotImplementedError("Implement bucket_gradient_allreduce")
