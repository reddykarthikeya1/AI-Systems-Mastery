"""Production solution for GramSchmidtQR."""
from __future__ import annotations

import numpy as np


class GramSchmidtQR:
    """Orthonormalization and QR decomposition via modified Gram-Schmidt."""

    @staticmethod
    def qr_factorization(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        A = np.asarray(A, dtype=float)
        m, n = A.shape
        Q = np.zeros((m, n), dtype=float)
        R = np.zeros((n, n), dtype=float)

        V = A.copy()
        for j in range(n):
            for i in range(j):
                R[i, j] = float(np.dot(Q[:, i], V[:, j]))
                V[:, j] -= R[i, j] * Q[:, i]

            R[j, j] = float(np.linalg.norm(V[:, j]))
            if np.isclose(R[j, j], 0.0):
                raise ValueError("Matrix columns are linearly dependent")
            Q[:, j] = V[:, j] / R[j, j]

        return Q, R

    @staticmethod
    def project_onto_subspace(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        A = np.asarray(A, dtype=float)
        b = np.asarray(b, dtype=float)
        # Using pseudo-inverse projection P = A @ (A^T A)^-1 @ A^T
        # Efficiently via QR: P @ b = Q @ Q^T @ b
        Q, _ = np.linalg.qr(A)
        return Q @ (Q.T @ b)
