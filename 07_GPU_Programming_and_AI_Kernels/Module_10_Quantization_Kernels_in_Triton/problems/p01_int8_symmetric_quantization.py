"""Problem 01 — Int8 Symmetric Quantization

Topic: 10 Quantization Kernels in Triton
Target: Production-grade implementation

Compute INT8 symmetric scale factor and quantize float vector to [-128, 127].

Example:
    >>> int8_symmetric_quantization([-64.0, 0.0, 32.0, 63.5])
    (0.5039, [-127, 0, 64, 126])

Hints:
    Hint 1: The scale must map the single largest-magnitude value in the
        vector onto the edge of the representable INT8 range, so every
        other value quantizes proportionally without overflowing.
    Hint 2: Set `scale = max(abs(x) for x in values) / 127.0`, then quantize
        each element as `round(x / scale)` clamped to `[-128, 127]` — note
        the range is asymmetric (127 positive, 128 negative) even though
        the scale itself is symmetric.
    Hint 3: A max magnitude of `0.0` (all-zero input, or an empty list)
        must fall back to `scale = 1.0` instead of dividing by zero, and
        rounding happens before clamping, not after, so a value that rounds
        just past 127 still gets clipped.
"""

from __future__ import annotations


def int8_symmetric_quantization(values: list[float]) -> tuple[float, list[int]]:
    """Scale factor: scale = max(abs(x) for x in values) / 127.0 (or 1.0 if max == 0).
    Quantized values: clamp(round(x / scale), -128, 127).
    Returns (scale rounded to 4 decimals, quantized_list).
    """
    raise NotImplementedError("Implement int8_symmetric_quantization")
