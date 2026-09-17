"""Problem 01 — Fp8 E4M3 Dequantize

Topic: 08 Quantization for Serving
Target: Production-grade implementation

Emulate FP8 E4M3 dequantization with per-tensor scale factor.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def fp8_e4m3_dequantize(q_integers: list[int], scale: float) -> list[float]:
    """Dequantize: val = q_int * scale.
    Returns list of float32 values rounded to 4 decimals.
    """
    raise NotImplementedError("Implement fp8_e4m3_dequantize")
