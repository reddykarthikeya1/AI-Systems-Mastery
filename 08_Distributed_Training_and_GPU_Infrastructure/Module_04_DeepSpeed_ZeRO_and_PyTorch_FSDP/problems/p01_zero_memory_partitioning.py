"""Problem 01 — Zero Memory Partitioning

Topic: 04 DeepSpeed ZeRO and PyTorch FSDP
Target: Production-grade implementation

Calculate memory footprint across ZeRO stages 1, 2, and 3.

Example:
    >>> zero_memory_partitioning(10.0, 64)
    {'baseline_gb': 160.0, 'zero_1_gb': 41.88, 'zero_2_gb': 22.19, 'zero_3_gb': 2.5}

Hints:
    Hint 1: Each successive ZeRO stage shards one more of the three
        per-parameter buffers (optimizer state, then gradients, then the
        parameters themselves) across `num_gpus`, so only the still-shared
        pieces stay at full size while the sharded pieces shrink by `/ N`.
    Hint 2: Work in bytes-per-parameter terms scaled by `param_count_
        billions`: params and grads are 2 bytes each, optimizer state is 12
        bytes (4+4+4 for fp32 weights/momentum/variance). Stage 1 shards
        only the 12-byte optimizer state; stage 2 shards optimizer+grad
        (14 bytes); stage 3 shards all 16 bytes.
    Hint 3: The unsharded portion in each stage is *not* divided by `N` —
        only the sharded portion is (e.g. ZeRO-1 keeps `2*p + 2*p` full-size
        and only divides the `12*p` optimizer term). Round every value in
        the result dict to 2 decimals.
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
