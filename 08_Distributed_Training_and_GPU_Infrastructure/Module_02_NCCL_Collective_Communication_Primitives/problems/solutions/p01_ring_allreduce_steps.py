"""Reference Solution — Problem 01: Ring Allreduce Steps

Topic: 02 NCCL Collective Communication Primitives
"""

from __future__ import annotations


def ring_allreduce_steps(data_size_bytes: int, num_gpus: int) -> dict[str, float]:
    if num_gpus <= 1:
        return {'scatter_bytes': 0.0, 'allgather_bytes': 0.0, 'total_bytes_per_gpu': 0.0}
    chunk = (num_gpus - 1) / float(num_gpus) * data_size_bytes
    return {
        'scatter_bytes': round(chunk, 2),
        'allgather_bytes': round(chunk, 2),
        'total_bytes_per_gpu': round(2.0 * chunk, 2)
    }
