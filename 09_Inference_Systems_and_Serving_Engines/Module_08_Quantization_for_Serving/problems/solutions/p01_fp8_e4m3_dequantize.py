"""Reference Solution — Problem 01: Fp8 E4M3 Dequantize

Topic: 08 Quantization for Serving
"""

from __future__ import annotations


def fp8_e4m3_dequantize(q_integers: list[int], scale: float) -> list[float]:
    return [round(x * scale, 4) for x in q_integers]
