"""Problem 01 — Gram Schmidt Orthogonalization

Topic: 04 Vector Spaces Bases and Rank
Target: Production-grade implementation

Compute orthogonal basis from linearly independent input vectors.

Example:
    >>> gram_schmidt_orthogonalization([[3.0, 1.0], [2.0, 2.0]])
    [[3.0, 1.0], [-0.4, 1.2]]

Hints:
    Hint 1: Each new orthogonal vector only needs to have zero dot product
        with every vector already produced — subtracting off the component
        of v_k that points along each earlier u_j is exactly what enforces
        that.
    Hint 2: Use the classical Gram-Schmidt formula as given: for each
        already-built u_j, compute the projection coefficient
        `dot(v_k, u_j) / dot(u_j, u_j)` and subtract `coeff * u_j` from the
        running vector, accumulating over all previous j before storing u_k.
    Hint 3: A near-zero `dot(u_j, u_j)` means u_j collapsed to (numerically)
        the zero vector — guard that division and skip the projection for
        it rather than dividing by ~0, and round every output component to
        4 decimal places.
"""

from __future__ import annotations


def gram_schmidt_orthogonalization(vectors: list[list[float]]) -> list[list[float]]:
    """Gram-Schmidt process:
    u_k = v_k - sum_{j < k} (proj_{u_j}(v_k))
    where proj_u(v) = (v . u / (u . u)) * u
    Returns list of orthogonal vectors u_k rounded to 4 decimals.
    """
    raise NotImplementedError("Implement gram_schmidt_orthogonalization")
