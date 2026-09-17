"""Problem 01 — Bootstrap Confidence Interval

Topic: 12 Statistical Estimation from Samples
Target: Production-grade implementation

Compute empirical bootstrap confidence interval percentiles.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bootstrap_confidence_interval(estimates: list[float], alpha: float = 0.05) -> tuple[float, float]:
    """Sort estimates and extract lower (alpha/2) and upper (1 - alpha/2) percentiles.
    Returns (lower_bound, upper_bound) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement bootstrap_confidence_interval")
