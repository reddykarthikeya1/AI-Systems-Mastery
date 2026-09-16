"""Production solution for PowerIterationPageRank."""
from __future__ import annotations

import numpy as np


class PowerIterationPageRank:
    """Eigenvalue and eigenvector computation via power iteration."""

    @staticmethod
    def dominant_eigen(
        A: np.ndarray, max_iter: int = 1000, tol: float = 1e-10
    ) -> tuple[float, np.ndarray]:
        A = np.asarray(A, dtype=float)
        n = A.shape[0]
        v = np.ones(n, dtype=float) / np.sqrt(n)

        eigenval = 0.0
        for _ in range(max_iter):
            w = A @ v
            norm_w = np.linalg.norm(w)
            if np.isclose(norm_w, 0.0):
                return 0.0, v

            v_new = w / norm_w
            new_eigenval = float(v_new.T @ A @ v_new)

            if np.abs(new_eigenval - eigenval) < tol:
                return new_eigenval, v_new

            v = v_new
            eigenval = new_eigenval

        return eigenval, v

    @staticmethod
    def compute_pagerank(
        adj_matrix: np.ndarray, damping: float = 0.85, max_iter: int = 200, tol: float = 1e-8
    ) -> np.ndarray:
        A = np.asarray(adj_matrix, dtype=float)
        n = A.shape[0]

        M = np.zeros_like(A)
        for j in range(n):
            s = np.sum(A[:, j])
            if s > 0:
                M[:, j] = A[:, j] / s
            else:
                M[:, j] = 1.0 / n

        # Google matrix with damping factor
        G = damping * M + ((1.0 - damping) / n) * np.ones((n, n))

        # Power iteration to find stationary distribution (pi = G @ pi)
        pi = np.ones(n, dtype=float) / n
        for _ in range(max_iter):
            pi_next = G @ pi
            if np.linalg.norm(pi_next - pi, ord=1) < tol:
                return pi_next
            pi = pi_next

        return pi
