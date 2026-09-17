"""Reference Solution — Problem 01: Truncated Svd Reconstruction

Topic: 07 LowRank Structure and Quadratic Forms
"""

from __future__ import annotations


def truncated_svd_reconstruction(sigma: float, u: list[float], v: list[float]) -> list[list[float]]:
    M = []
    for ui in u:
        row = [round(sigma * ui * vj, 4) for vj in v]
        M.append(row)
    return M
