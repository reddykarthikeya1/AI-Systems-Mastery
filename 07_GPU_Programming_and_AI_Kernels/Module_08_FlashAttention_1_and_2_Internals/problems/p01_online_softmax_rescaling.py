"""Problem 01 — Online Softmax Rescaling

Topic: 08 FlashAttention 1 and 2 Internals
Target: Production-grade implementation

Combine two softmax blocks with online max rescaling for FlashAttention.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def online_softmax_rescaling(max1: float, sum1: float, max2: float, sum2: float) -> tuple[float, float]:
    """FlashAttention online softmax rescaling:
    new_max = max(max1, max2)
    new_sum = sum1 * exp(max1 - new_max) + sum2 * exp(max2 - new_max)
    Returns (new_max, new_sum) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement online_softmax_rescaling")
