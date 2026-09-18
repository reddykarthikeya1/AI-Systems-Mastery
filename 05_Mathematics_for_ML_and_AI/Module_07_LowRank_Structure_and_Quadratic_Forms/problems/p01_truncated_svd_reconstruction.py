"""Problem 01 — Truncated Svd Reconstruction

Topic: 07 LowRank Structure and Quadratic Forms
Target: Production-grade implementation

Reconstruct low-rank matrix from top-1 singular value and singular vectors.

Example:
    >>> truncated_svd_reconstruction(10.0, [1.0, 0.5], [1.0, 2.0])
    [[10.0, 20.0], [5.0, 10.0]]

Hints:
    Hint 1: A rank-1 matrix is completely determined by one scalar and two
        vectors: every entry is just a scaled product of one component from
        each vector, so there's no matrix multiplication machinery needed.
    Hint 2: Build the outer product directly: entry (i, j) of the result is
        `sigma * u[i] * v[j]`, so iterate rows over `u` and columns over `v`.
    Hint 3: The output shape is `len(u)` rows by `len(v)` columns — u and v
        need not be the same length (rectangular A is fine) — and each
        entry should be rounded to 4 decimal places independently.
"""

from __future__ import annotations


def truncated_svd_reconstruction(sigma: float, u: list[float], v: list[float]) -> list[list[float]]:
    """Compute outer product rank-1 approximation A_approx = sigma * (u (x) v^T).
    Returns 2D matrix rounded to 4 decimals.
    """
    raise NotImplementedError("Implement truncated_svd_reconstruction")
