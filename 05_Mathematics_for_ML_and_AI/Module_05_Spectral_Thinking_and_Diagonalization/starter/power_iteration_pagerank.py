"""Starter template for PowerIterationPageRank."""
from __future__ import annotations

import numpy as np


class PowerIterationPageRank:
    """Eigenvalue and eigenvector computation via power iteration."""

    @staticmethod
    def dominant_eigen(
        A: np.ndarray, max_iter: int = 1000, tol: float = 1e-10
    ) -> tuple[float, np.ndarray]:
        """Compute the largest eigenvalue and associated unit eigenvector."""
        raise NotImplementedError

    @staticmethod
    def compute_pagerank(
        adj_matrix: np.ndarray, damping: float = 0.85, max_iter: int = 200, tol: float = 1e-8
    ) -> np.ndarray:
        """Compute PageRank probability distribution vector using power iteration."""
        raise NotImplementedError
