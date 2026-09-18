"""Problem 01 — Ring Allreduce Steps

Topic: 02 NCCL Collective Communication Primitives
Target: Production-grade implementation

Calculate scatter-reduce and allgather data transfer volumes for N GPUs.

Example:
    >>> ring_allreduce_steps(8000, 8)
    {'scatter_bytes': 7000.0, 'allgather_bytes': 7000.0, 'total_bytes_per_gpu': 14000.0}

Hints:
    Hint 1: In a ring AllReduce every GPU only ever needs to send the
        fraction of the data it *doesn't* already hold — with N GPUs
        sharing the buffer, that's `(N - 1) / N` of it, per phase.
    Hint 2: Compute `chunk = (num_gpus - 1) / num_gpus * data_size_bytes`;
        both the scatter-reduce and allgather phases move exactly `chunk`
        bytes per GPU, and the total per GPU is `2 * chunk`.
    Hint 3: `num_gpus <= 1` means there's nothing to reduce across, so all
        three values must come back as `0.0` instead of doing a
        division that would otherwise still succeed but be meaningless.
        Round every value in the returned dict to 2 decimals.
"""

from __future__ import annotations


def ring_allreduce_steps(data_size_bytes: int, num_gpus: int) -> dict[str, float]:
    """Ring AllReduce transfers 2 * (N - 1) / N * data_size_bytes per GPU.
    Scatter-reduce phase: (N - 1) / N * data_size_bytes
    Allgather phase: (N - 1) / N * data_size_bytes
    Returns dict with 'scatter_bytes', 'allgather_bytes', 'total_bytes_per_gpu'.
    """
    raise NotImplementedError("Implement ring_allreduce_steps")
