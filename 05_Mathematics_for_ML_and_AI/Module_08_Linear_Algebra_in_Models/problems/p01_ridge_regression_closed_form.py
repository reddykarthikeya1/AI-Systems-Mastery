"""Problem 01 — Ridge Regression Closed Form

Topic: 08 Linear Algebra in Models
Target: Production-grade implementation

Compute 1D ridge regression regularized slope: w = (X^T X + lambda)^(-1) X^T y.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ridge_regression_closed_form(X: list[float], y: list[float], lmbda: float = 1.0) -> float:
    """1D ridge regression without bias:
    w = sum(x * y) / (sum(x * x) + lmbda)
    Returns slope w rounded to 4 decimals.
    """
    raise NotImplementedError("Implement ridge_regression_closed_form")
