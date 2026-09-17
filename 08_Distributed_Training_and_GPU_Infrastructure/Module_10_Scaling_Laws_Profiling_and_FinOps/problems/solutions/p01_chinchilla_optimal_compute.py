"""Reference Solution — Problem 01: Chinchilla Optimal Compute

Topic: 10 Scaling Laws Profiling and FinOps
"""

from __future__ import annotations


def chinchilla_optimal_compute(flop_budget: float) -> tuple[float, float]:
    import math
    if flop_budget <= 0:
        return (0.0, 0.0)
    opt = math.sqrt(flop_budget / 6.0)
    return (round(opt, 2), round(opt, 2))
