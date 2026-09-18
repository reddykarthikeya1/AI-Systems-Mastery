"""Problem 01 — Online Softmax Rescaling

Topic: 08 FlashAttention 1 and 2 Internals
Target: Production-grade implementation

Combine two softmax blocks with online max rescaling for FlashAttention.

Example:
    >>> online_softmax_rescaling(5.0, 2.0, 10.0, 3.0)
    (10.0, 3.0135)

Hints:
    Hint 1: Each block's `sum` was accumulated relative to its *own* max,
        so the two sums can't just be added — they first need to be
        re-based onto a shared, common max.
    Hint 2: Take `new_max = max(max1, max2)`, then rescale each block's sum
        by `exp(block_max - new_max)` before adding the two rescaled sums
        together — this is the standard log-sum-exp shift trick.
    Hint 3: When a block's max already equals `new_max`, its rescale factor
        is `exp(0) == 1` (no change); the other block's factor is `< 1` and
        shrinks its contribution accordingly. Round both `new_max` and the
        combined sum to 4 decimals.
"""

from __future__ import annotations


def online_softmax_rescaling(max1: float, sum1: float, max2: float, sum2: float) -> tuple[float, float]:
    """FlashAttention online softmax rescaling:
    new_max = max(max1, max2)
    new_sum = sum1 * exp(max1 - new_max) + sum2 * exp(max2 - new_max)
    Returns (new_max, new_sum) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement online_softmax_rescaling")
