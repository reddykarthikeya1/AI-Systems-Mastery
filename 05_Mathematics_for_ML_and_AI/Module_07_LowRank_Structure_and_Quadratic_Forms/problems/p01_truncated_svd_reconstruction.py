"""Problem 01 — Truncated Svd Reconstruction

Topic: 07 LowRank Structure and Quadratic Forms
Target: Production-grade implementation

Reconstruct low-rank matrix from top-1 singular value and singular vectors.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def truncated_svd_reconstruction(sigma: float, u: list[float], v: list[float]) -> list[list[float]]:
    """Compute outer product rank-1 approximation A_approx = sigma * (u (x) v^T).
    Returns 2D matrix rounded to 4 decimals.
    """
    raise NotImplementedError("Implement truncated_svd_reconstruction")
