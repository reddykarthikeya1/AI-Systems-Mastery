"""Reference Solution — Problem 01: Online Softmax Rescaling

Topic: 08 FlashAttention 1 and 2 Internals
"""

from __future__ import annotations


def online_softmax_rescaling(max1: float, sum1: float, max2: float, sum2: float) -> tuple[float, float]:
    import math
    new_max = max(max1, max2)
    s1_scaled = sum1 * math.exp(max1 - new_max)
    s2_scaled = sum2 * math.exp(max2 - new_max)
    return (round(new_max, 4), round(s1_scaled + s2_scaled, 4))
