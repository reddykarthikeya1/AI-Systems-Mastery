"""Starter template for BasisRankNullspace."""
from __future__ import annotations

import numpy as np


class BasisRankNullspace:
    """Vector space basis, matrix rank, and nullspace analyzer."""

    @staticmethod
    def matrix_rank(A: np.ndarray, tol: float = 1e-10) -> int:
        """Compute the rank of matrix A (number of non-zero singular values)."""
        raise NotImplementedError

    @staticmethod
    def is_linearly_independent(vectors: list[np.ndarray], tol: float = 1e-10) -> bool:
        """Return True if the set of vectors is linearly independent."""
        raise NotImplementedError

    @staticmethod
    def nullspace_basis(A: np.ndarray, tol: float = 1e-10) -> np.ndarray:
        """Return orthonormal basis for the nullspace N(A) such that A @ v = 0."""
        raise NotImplementedError
