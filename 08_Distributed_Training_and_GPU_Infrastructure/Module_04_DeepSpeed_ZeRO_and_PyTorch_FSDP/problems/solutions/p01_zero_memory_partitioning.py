"""Reference Solution — Problem 01: Zero Memory Partitioning

Topic: 04 DeepSpeed ZeRO and PyTorch FSDP
"""

from __future__ import annotations


def zero_memory_partitioning(param_count_billions: float, num_gpus: int) -> dict[str, float]:
    p = param_count_billions
    n = float(num_gpus)
    base = 16.0 * p
    z1 = 2.0 * p + 2.0 * p + (12.0 * p / n)
    z2 = 2.0 * p + (14.0 * p / n)
    z3 = 16.0 * p / n
    return {
        'baseline_gb': round(base, 2),
        'zero_1_gb': round(z1, 2),
        'zero_2_gb': round(z2, 2),
        'zero_3_gb': round(z3, 2)
    }
