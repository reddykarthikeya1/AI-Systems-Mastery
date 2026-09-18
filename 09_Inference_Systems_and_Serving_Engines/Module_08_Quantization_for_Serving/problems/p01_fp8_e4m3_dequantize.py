"""Problem 01 — Fp8 E4M3 Dequantize

Topic: 08 Quantization for Serving
Target: Production-grade implementation

Emulate FP8 E4M3 dequantization with per-tensor scale factor.

Example:
    >>> fp8_e4m3_dequantize([10, -5, 0], 0.05)
    [0.5, -0.25, 0.0]

Hints:
    Hint 1: Dequantization here is a simple affine rescale — every stored
        integer code maps back to a real value through the same shared
        per-tensor `scale`, independently of the other elements.
    Hint 2: A single list comprehension multiplying each element of
        `q_integers` by `scale` is all this needs — no per-element
        branching or lookup structure.
    Hint 3: Round each result to 4 decimal places individually (not the
        whole list at once, and not by truncation), and treat negative
        codes and zero the same as positive ones with no special-casing —
        the tests compare the rounded floats exactly.
"""

from __future__ import annotations


def fp8_e4m3_dequantize(q_integers: list[int], scale: float) -> list[float]:
    """Dequantize: val = q_int * scale.
    Returns list of float32 values rounded to 4 decimals.
    """
    raise NotImplementedError("Implement fp8_e4m3_dequantize")
