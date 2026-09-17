"""Problem 01 — Property-Based Matrix Invariant

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def verify_matrix_symmetry(matrix: list[list[int]]) -> bool:
    n = len(matrix)
    if n == 0: return True
    if any(len(row) != n for row in matrix): return False
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True
