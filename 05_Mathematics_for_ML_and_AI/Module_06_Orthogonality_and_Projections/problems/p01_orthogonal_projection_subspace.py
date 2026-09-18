"""Problem 01 — Orthogonal Projection Subspace

Topic: 06 Orthogonality and Projections
Target: Production-grade implementation

Project vector onto subspace defined by orthonormal basis vectors.

Example:
    >>> orthogonal_projection_subspace([3.0, 4.0], [[1.0, 0.0]])
    [3.0, 0.0]

Hints:
    Hint 1: Because the basis is orthonormal, the projection onto the whole
        subspace is simply the sum of the independent projections onto each
        basis vector — there's no cross-term correction to worry about.
    Hint 2: For each basis vector `u`, compute the scalar coefficient
        `v . u` (no division needed since `u . u == 1`), then accumulate
        `coeff * u` component-wise into the running result vector.
    Hint 3: Accumulate into a zero-initialized result vector across ALL
        basis vectors before rounding — rounding each partial term early
        would compound rounding error across multiple basis vectors. Round
        only the final summed components to 4 decimal places.
"""

from __future__ import annotations


def orthogonal_projection_subspace(v: list[float], basis: list[list[float]]) -> list[float]:
    """Compute proj_V(v) = sum_{u in basis} (v . u) * u.
    Returns projected vector rounded to 4 decimals.
    """
    raise NotImplementedError("Implement orthogonal_projection_subspace")
