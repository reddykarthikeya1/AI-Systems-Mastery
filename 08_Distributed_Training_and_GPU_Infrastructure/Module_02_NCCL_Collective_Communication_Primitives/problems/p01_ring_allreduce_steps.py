"""Problem 01 — Ring Allreduce Steps

Topic: 02 NCCL Collective Communication Primitives
Target: Production-grade implementation

Calculate scatter-reduce and allgather data transfer volumes for N GPUs.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ring_allreduce_steps(data_size_bytes: int, num_gpus: int) -> dict[str, float]:
    """Ring AllReduce transfers 2 * (N - 1) / N * data_size_bytes per GPU.
    Scatter-reduce phase: (N - 1) / N * data_size_bytes
    Allgather phase: (N - 1) / N * data_size_bytes
    Returns dict with 'scatter_bytes', 'allgather_bytes', 'total_bytes_per_gpu'.
    """
    raise NotImplementedError("Implement ring_allreduce_steps")
