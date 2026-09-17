"""Problem 01 — Orthogonal Projection Subspace

Topic: 06 Orthogonality and Projections
Target: Production-grade implementation

Project vector onto subspace defined by orthonormal basis vectors.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def orthogonal_projection_subspace(v: list[float], basis: list[list[float]]) -> list[float]:
    """Compute proj_V(v) = sum_{u in basis} (v . u) * u.
    Returns projected vector rounded to 4 decimals.
    """
    raise NotImplementedError("Implement orthogonal_projection_subspace")
