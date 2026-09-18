"""Problem 01 — Bootstrap Confidence Interval

Topic: 12 Statistical Estimation from Samples
Target: Production-grade implementation

Compute empirical bootstrap confidence interval percentiles.

Example:
    >>> bootstrap_confidence_interval([float(i) for i in range(20)], alpha=0.1)
    (1.0, 18.0)

Hints:
    Hint 1: A percentile of a sample is just "the value at a certain
        position once everything is sorted" — no distributional assumption
        is needed, which is the whole point of a bootstrap interval.
    Hint 2: Sort the estimates, then index into the sorted list at position
        `alpha/2 * n` for the lower bound and `(1 - alpha/2) * n` for the
        upper bound (converted to integer indices).
    Hint 3: The naive upper-bound index formula can land exactly at `n`
        (one past the last element) or the naive lower index can go
        negative for extreme alpha — clamp both indices into `[0, n - 1]`
        before indexing, and round both returned bounds to 4 decimals.
"""

from __future__ import annotations


def bootstrap_confidence_interval(estimates: list[float], alpha: float = 0.05) -> tuple[float, float]:
    """Sort estimates and extract lower (alpha/2) and upper (1 - alpha/2) percentiles.
    Returns (lower_bound, upper_bound) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement bootstrap_confidence_interval")
