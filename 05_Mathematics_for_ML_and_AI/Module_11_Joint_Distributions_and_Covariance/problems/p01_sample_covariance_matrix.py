"""Problem 01 — Sample Covariance Matrix

Topic: 11 Joint Distributions and Covariance
Target: Production-grade implementation

Compute 2x2 sample covariance matrix between two numerical series.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def sample_covariance_matrix(x: list[float], y: list[float]) -> list[list[float]]:
    """Compute sample covariance matrix [[cov(x,x), cov(x,y)], [cov(y,x), cov(y,y)]].
    Formula: cov(a, b) = sum((ai - mean(a)) * (bi - mean(b))) / (N - 1)
    Returns 2x2 matrix rounded to 4 decimals.
    """
    raise NotImplementedError("Implement sample_covariance_matrix")
