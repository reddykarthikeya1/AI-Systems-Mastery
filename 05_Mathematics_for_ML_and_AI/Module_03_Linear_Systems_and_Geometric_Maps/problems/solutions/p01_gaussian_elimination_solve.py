"""Reference Solution — Problem 01: Gaussian Elimination Solve

Topic: 03 Linear Systems and Geometric Maps
"""

from __future__ import annotations


def gaussian_elimination_solve(A: list[list[float]], b: list[float]) -> list[float]:
    n = len(A)
    # Augmented matrix
    M = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        # Pivot
        pivot = M[i][i]
        if abs(pivot) < 1e-9:
            for k in range(i + 1, n):
                if abs(M[k][i]) > 1e-9:
                    M[i], M[k] = M[k], M[i]
                    pivot = M[i][i]
                    break
        for j in range(i + 1, n):
            factor = M[j][i] / pivot
            for col in range(i, n + 1):
                M[j][col] -= factor * M[i][col]
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = round((M[i][n] - s) / M[i][i], 4)
    return x
