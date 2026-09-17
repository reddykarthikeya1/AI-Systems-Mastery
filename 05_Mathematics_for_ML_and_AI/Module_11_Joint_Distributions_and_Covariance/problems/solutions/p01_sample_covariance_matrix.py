"""Reference Solution — Problem 01: Sample Covariance Matrix

Topic: 11 Joint Distributions and Covariance
"""

from __future__ import annotations


def sample_covariance_matrix(x: list[float], y: list[float]) -> list[list[float]]:
    n = len(x)
    if n < 2:
        return [[0.0, 0.0], [0.0, 0.0]]
    mx = sum(x) / n
    my = sum(y) / n
    c_xx = sum((xi - mx) ** 2 for xi in x) / (n - 1)
    c_yy = sum((yi - my) ** 2 for yi in y) / (n - 1)
    c_xy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)
    return [[round(c_xx, 4), round(c_xy, 4)], [round(c_xy, 4), round(c_yy, 4)]]
