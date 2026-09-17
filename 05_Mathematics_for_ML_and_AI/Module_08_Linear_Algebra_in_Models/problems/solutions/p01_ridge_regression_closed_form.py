"""Reference Solution — Problem 01: Ridge Regression Closed Form

Topic: 08 Linear Algebra in Models
"""

from __future__ import annotations


def ridge_regression_closed_form(X: list[float], y: list[float], lmbda: float = 1.0) -> float:
    xty = sum(x * yi for x, yi in zip(X, y))
    xtx = sum(x * x for x in X)
    w = xty / (xtx + lmbda)
    return round(w, 4)
