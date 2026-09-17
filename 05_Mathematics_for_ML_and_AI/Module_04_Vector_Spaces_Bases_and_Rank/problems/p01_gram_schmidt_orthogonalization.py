"""Problem 01 — Gram Schmidt Orthogonalization

Topic: 04 Vector Spaces Bases and Rank
Target: Production-grade implementation

Compute orthogonal basis from linearly independent input vectors.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def gram_schmidt_orthogonalization(vectors: list[list[float]]) -> list[list[float]]:
    """Gram-Schmidt process:
    u_k = v_k - sum_{j < k} (proj_{u_j}(v_k))
    where proj_u(v) = (v . u / (u . u)) * u
    Returns list of orthogonal vectors u_k rounded to 4 decimals.
    """
    raise NotImplementedError("Implement gram_schmidt_orthogonalization")
