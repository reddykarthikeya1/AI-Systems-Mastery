"""Starter template for GaussianEliminationSolver."""
from __future__ import annotations

import numpy as np


class GaussianEliminationSolver:
    """Linear system solver using Gaussian elimination with partial pivoting."""

    @staticmethod
    def solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Solve Ax = b. Raises ValueError if matrix is singular or shapes mismatch."""
        raise NotImplementedError

    @staticmethod
    def determinant(A: np.ndarray) -> float:
        """Compute determinant via triangular decomposition from elimination."""
        raise NotImplementedError
