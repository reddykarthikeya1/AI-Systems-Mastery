"""Production solution for GaussianEliminationSolver."""
from __future__ import annotations

import numpy as np


class GaussianEliminationSolver:
    """Linear system solver using Gaussian elimination with partial pivoting."""

    @staticmethod
    def solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        n = A.shape[0]
        if A.shape[1] != n or b.shape[0] != n:
            raise ValueError("Matrix A must be square and match dimensions of vector b")

        # Augmented matrix [A | b]
        aug = np.hstack([A, b.reshape(-1, 1)])

        # Forward elimination with partial pivoting
        for col in range(n):
            pivot_row = col + int(np.argmax(np.abs(aug[col:, col])))
            if np.isclose(aug[pivot_row, col], 0.0):
                raise ValueError("Matrix is singular or near-singular (no unique solution)")

            if pivot_row != col:
                aug[[col, pivot_row]] = aug[[pivot_row, col]]

            for r in range(col + 1, n):
                factor = aug[r, col] / aug[col, col]
                aug[r, col:] -= factor * aug[col, col:]

        # Back-substitution
        x = np.zeros(n, dtype=float)
        for r in range(n - 1, -1, -1):
            x[r] = (aug[r, -1] - np.dot(aug[r, r + 1:n], x[r + 1:n])) / aug[r, r]

        return x

    @staticmethod
    def determinant(A: np.ndarray) -> float:
        A = np.array(A, dtype=float)
        n = A.shape[0]
        if A.shape[1] != n:
            raise ValueError("Matrix must be square to compute determinant")

        det = 1.0
        mat = A.copy()

        for col in range(n):
            pivot_row = col + int(np.argmax(np.abs(mat[col:, col])))
            if np.isclose(mat[pivot_row, col], 0.0):
                return 0.0

            if pivot_row != col:
                mat[[col, pivot_row]] = mat[[pivot_row, col]]
                det *= -1.0  # Row swap negates determinant

            pivot = mat[col, col]
            det *= pivot

            for r in range(col + 1, n):
                factor = mat[r, col] / pivot
                mat[r, col:] -= factor * mat[col, col:]

        return float(det)
