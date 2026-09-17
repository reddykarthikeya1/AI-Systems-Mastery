"""Reference Solution — Problem 01: Orthogonal Projection Subspace

Topic: 06 Orthogonality and Projections
"""

from __future__ import annotations


def orthogonal_projection_subspace(v: list[float], basis: list[list[float]]) -> list[float]:
    res = [0.0] * len(v)
    for u in basis:
        coeff = sum(x * y for x, y in zip(v, u))
        for i in range(len(v)):
            res[i] += coeff * u[i]
    return [round(x, 4) for x in res]
