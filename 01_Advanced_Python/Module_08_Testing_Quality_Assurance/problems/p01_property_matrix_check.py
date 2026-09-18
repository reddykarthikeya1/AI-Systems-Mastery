"""Problem 01 — Property-Based Matrix Invariant

Target: Production-grade implementation

Example:
    >>> verify_matrix_symmetry([[1, 2], [2, 1]])
    True
    >>> verify_matrix_symmetry([[1, 2], [3, 1]])
    False

Hints:
    Hint 1: A matrix is symmetric exactly when it equals its own transpose,
        so you only need to compare each off-diagonal pair once, not the
        whole grid twice.
    Hint 2: Use the square dimension `n = len(matrix)` and a nested loop over
        `i` and `j > i`, comparing `matrix[i][j]` against `matrix[j][i]`.
    Hint 3: An empty matrix (`[]`) counts as trivially symmetric and must
        return `True`, and any row whose length differs from `n` (a ragged,
        non-square matrix) must return `False` rather than raising an
        `IndexError`.
"""

from __future__ import annotations


def verify_matrix_symmetry(matrix: list[list[int]]) -> bool:
    raise NotImplementedError('Implement verify_matrix_symmetry')
