"""Production solution for BasisRankNullspace."""
from __future__ import annotations

import numpy as np


class BasisRankNullspace:
    """Vector space basis, matrix rank, and nullspace analyzer using SVD."""

    @staticmethod
    def matrix_rank(A: np.ndarray, tol: float = 1e-10) -> int:
        A = np.asarray(A, dtype=float)
        if A.size == 0:
            return 0
        _, s, _ = np.linalg.svd(A)
        return int(np.sum(s > tol))

    @staticmethod
    def is_linearly_independent(vectors: list[np.ndarray], tol: float = 1e-10) -> bool:
        if not vectors:
            return True
        # Stack vectors as columns
        mat = np.column_stack(vectors)
        rank = BasisRankNullspace.matrix_rank(mat, tol=tol)
        return rank == len(vectors)

    @staticmethod
    def nullspace_basis(A: np.ndarray, tol: float = 1e-10) -> np.ndarray:
        A = np.asarray(A, dtype=float)
        _, s, vh = np.linalg.svd(A)
        # Nullspace corresponds to right singular vectors (rows of vh) with zero singular values
        num_singular = np.sum(s > tol)
        null_basis = vh[num_singular:]
        return null_basis.T  # Columns are basis vectors
