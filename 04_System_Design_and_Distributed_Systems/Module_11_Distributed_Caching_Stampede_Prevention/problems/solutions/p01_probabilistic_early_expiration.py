"""Reference Solution — Problem 01: Probabilistic Early Expiration

Topic: 11 Distributed Caching Stampede Prevention
"""

from __future__ import annotations


def probabilistic_early_expiration(read_time: float, expiry_time: float, compute_cost: float, beta: float = 1.0, rand_val: float = 0.5) -> bool:
    import math
    if rand_val <= 0.0:
        return True
    return (read_time - compute_cost * beta * math.log(rand_val)) >= expiry_time
