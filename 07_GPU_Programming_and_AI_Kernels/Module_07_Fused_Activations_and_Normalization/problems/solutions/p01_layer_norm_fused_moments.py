"""Reference Solution — Problem 01: Layer Norm Fused Moments

Topic: 07 Fused Activations and Normalization
"""

from __future__ import annotations


def layer_norm_fused_moments(values: list[float]) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    count = 0
    mean = 0.0
    M2 = 0.0
    for x in values:
        count += 1
        delta = x - mean
        mean += delta / count
        delta2 = x - mean
        M2 += delta * delta2
    variance = M2 / count if count > 0 else 0.0
    return (round(mean, 4), round(variance, 4))
