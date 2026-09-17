"""Reference Solution — Problem 01: Softmax Stable Derivatives

Topic: 01 Math Fundamentals
"""

from __future__ import annotations


def softmax_stable_derivatives(logits: list[float]) -> list[float]:
    import math
    if not logits:
        return []
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps)
    return [round(e / s, 4) for e in exps]
