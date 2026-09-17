"""Problem 01 — Zero Memory Partitioning

Topic: 04 DeepSpeed ZeRO and PyTorch FSDP
Target: Production-grade implementation

Calculate memory footprint across ZeRO stages 1, 2, and 3.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def zero_memory_partitioning(param_count_billions: float, num_gpus: int) -> dict[str, float]:
    """FP16 model parameters: 2 bytes/param.
    Adam optimizer states: 12 bytes/param (FP32 master weights 4B, momentum 4B, variance 4B).
    Gradients: 2 bytes/param.
    Base memory GB = 16 * param_count_billions.
    ZeRO-1 (shards optimizer): 2 + 2 + 12 / N GB
    ZeRO-2 (shards optimizer + grad): 2 + 14 / N GB
    ZeRO-3 (shards optimizer + grad + params): 16 / N GB
    Returns dict mapping 'baseline_gb', 'zero_1_gb', 'zero_2_gb', 'zero_3_gb' per GPU rounded to 2 decimals.
    """
    raise NotImplementedError("Implement zero_memory_partitioning")
