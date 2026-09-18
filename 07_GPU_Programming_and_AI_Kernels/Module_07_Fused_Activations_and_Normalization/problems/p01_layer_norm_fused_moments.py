"""Problem 01 — Layer Norm Fused Moments

Topic: 07 Fused Activations and Normalization
Target: Production-grade implementation

Compute streaming mean and variance using Welford's one-pass algorithm.

Example:
    >>> layer_norm_fused_moments([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    (5.0, 4.0)

Hints:
    Hint 1: The point of Welford's method is getting both moments from a
        single pass over the data, without ever materializing a separate
        sum-of-squares that could lose precision on large values.
    Hint 2: Track a running `count`, `mean`, and `M2` (sum of squared
        deviations from the running mean). For each new `x`: increment
        `count`, update `mean` by `delta / count` where `delta = x - mean`,
        then accumulate `M2 += delta * (x - mean)` using the *updated*
        mean.
    Hint 3: Variance is `M2 / count` (population variance, not the `count -
        1` sample variance), and an empty input must return `(0.0, 0.0)`
        instead of dividing by zero. Round both outputs to 4 decimals.
"""

from __future__ import annotations


def layer_norm_fused_moments(values: list[float]) -> tuple[float, float]:
    """Compute (mean, variance) in single pass.
    Returns (mean, variance) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement layer_norm_fused_moments")
