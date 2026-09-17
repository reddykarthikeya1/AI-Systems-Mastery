"""Reference Solution — Problem 01: Shared Memory Gemm Tiling

Topic: 05 Tiled Matrix Multiplication GEMM
"""

from __future__ import annotations


def shared_memory_gemm_tiling(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = round(sum(A[i][k] * B[k][j] for k in range(n)), 4)
    return C
