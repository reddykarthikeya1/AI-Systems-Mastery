"""Reference Solution — Problem 01: Int8 Symmetric Quantization

Topic: 10 Quantization Kernels in Triton
"""

from __future__ import annotations


def int8_symmetric_quantization(values: list[float]) -> tuple[float, list[int]]:
    if not values:
        return (1.0, [])
    max_val = max(abs(x) for x in values)
    scale = (max_val / 127.0) if max_val > 0 else 1.0
    q = [max(-128, min(127, int(round(x / scale)))) for x in values]
    return (round(scale, 4), q)
