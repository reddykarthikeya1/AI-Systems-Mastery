"""Problem 01 — Sample Covariance Matrix

Topic: 11 Joint Distributions and Covariance
Target: Production-grade implementation

Compute 2x2 sample covariance matrix between two numerical series.

Example:
    >>> sample_covariance_matrix([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
    [[1.0, 2.0], [2.0, 4.0]]

Hints:
    Hint 1: The matrix is symmetric — cov(x, y) and cov(y, x) are the same
        computation, so you only need to derive one cross term and mirror
        it into both off-diagonal slots.
    Hint 2: Center each series on its own mean first (`xi - mean(x)`,
        `yi - mean(y)`), then average the products of centered values using
        the sample (Bessel-corrected) denominator `N - 1`, not `N`.
    Hint 3: With fewer than 2 observations, `N - 1` is zero or negative and
        the division is undefined — return the zero matrix
        `[[0.0, 0.0], [0.0, 0.0]]` in that case, and round every entry of
        the normal-case result to 4 decimal places.
"""

from __future__ import annotations


def sample_covariance_matrix(x: list[float], y: list[float]) -> list[list[float]]:
    """Compute sample covariance matrix [[cov(x,x), cov(x,y)], [cov(y,x), cov(y,y)]].
    Formula: cov(a, b) = sum((ai - mean(a)) * (bi - mean(b))) / (N - 1)
    Returns 2x2 matrix rounded to 4 decimals.
    """
    raise NotImplementedError("Implement sample_covariance_matrix")
