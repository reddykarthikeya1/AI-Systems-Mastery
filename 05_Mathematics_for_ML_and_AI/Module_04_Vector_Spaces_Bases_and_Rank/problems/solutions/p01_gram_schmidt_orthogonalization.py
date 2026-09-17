"""Reference Solution — Problem 01: Gram Schmidt Orthogonalization

Topic: 04 Vector Spaces Bases and Rank
"""

from __future__ import annotations


def gram_schmidt_orthogonalization(vectors: list[list[float]]) -> list[list[float]]:
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))
    u_list = []
    for v in vectors:
        u = v[:]
        for prev_u in u_list:
            denom = dot(prev_u, prev_u)
            if denom > 1e-9:
                coeff = dot(v, prev_u) / denom
                u = [x - coeff * y for x, y in zip(u, prev_u)]
        u_list.append([round(x, 4) for x in u])
    return u_list
