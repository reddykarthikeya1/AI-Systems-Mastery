"""Problem 01 — Ridge Regression Closed Form

Topic: 08 Linear Algebra in Models
Target: Production-grade implementation

Compute 1D ridge regression regularized slope: w = (X^T X + lambda)^(-1) X^T y.

Example:
    >>> ridge_regression_closed_form([1.0, 2.0, 3.0], [2.0, 4.0, 6.0], lmbda=5.0)
    1.4737

Hints:
    Hint 1: In one dimension the normal equations collapse to plain scalars,
        so the "matrix inverse" in the formula is just a single division —
        no matrix machinery is actually needed here.
    Hint 2: Compute `sum(x * y)` for the numerator and `sum(x * x)` for the
        denominator, add `lmbda` to the denominator before dividing, and
        that gives the regularized slope directly.
    Hint 3: With `lmbda=0.0` this must reduce exactly to ordinary
        least-squares (matching the unregularized slope), and any `lmbda >
        0` should shrink the magnitude of w toward zero versus that
        unregularized value — round the final result to 4 decimal places.
"""

from __future__ import annotations


def ridge_regression_closed_form(X: list[float], y: list[float], lmbda: float = 1.0) -> float:
    """1D ridge regression without bias:
    w = sum(x * y) / (sum(x * x) + lmbda)
    Returns slope w rounded to 4 decimals.
    """
    raise NotImplementedError("Implement ridge_regression_closed_form")
