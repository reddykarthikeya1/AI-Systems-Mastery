"""Problem 01 — Int8 Symmetric Quantization

Topic: 10 Quantization Kernels in Triton
Target: Production-grade implementation

Compute INT8 symmetric scale factor and quantize float vector to [-128, 127].

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def int8_symmetric_quantization(values: list[float]) -> tuple[float, list[int]]:
    """Scale factor: scale = max(abs(x) for x in values) / 127.0 (or 1.0 if max == 0).
    Quantized values: clamp(round(x / scale), -128, 127).
    Returns (scale rounded to 4 decimals, quantized_list).
    """
    raise NotImplementedError("Implement int8_symmetric_quantization")
