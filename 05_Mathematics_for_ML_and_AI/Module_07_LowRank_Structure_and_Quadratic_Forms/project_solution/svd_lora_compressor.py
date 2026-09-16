"""Production solution for SVD and LoRA compressor."""
from __future__ import annotations

import numpy as np


class SVDLoRACompressor:
    """Low-rank matrix approximation, LoRA factorization, and quadratic forms."""

    @staticmethod
    def truncate_svd(A: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        A = np.asarray(A, dtype=float)
        u, s, vh = np.linalg.svd(A, full_matrices=False)
        k = min(rank, len(s))
        return u[:, :k], s[:k], vh[:k, :]

    @staticmethod
    def energy_retention(singular_values: np.ndarray, rank: int) -> float:
        s = np.asarray(singular_values, dtype=float)
        total_energy = np.sum(s**2)
        if total_energy == 0:
            return 1.0
        k = min(rank, len(s))
        retained_energy = np.sum(s[:k] ** 2)
        return float(retained_energy / total_energy)

    @staticmethod
    def lora_factorize(W: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray]:
        W = np.asarray(W, dtype=float)
        u_k, s_k, vh_k = SVDLoRACompressor.truncate_svd(W, rank)
        # Absorb sqrt(singular_values) equally into B and A
        sqrt_s = np.sqrt(s_k)
        B = u_k * sqrt_s[None, :]  # shape (m, rank)
        A = sqrt_s[:, None] * vh_k  # shape (rank, n)
        return B, A

    @staticmethod
    def is_positive_definite(A: np.ndarray, tol: float = 1e-10) -> bool:
        A = np.asarray(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        # Check symmetry
        if not np.allclose(A, A.T, atol=tol):
            return False
        # Check eigenvalues > tol
        evals = np.linalg.eigvalsh(A)
        return bool(np.all(evals > tol))

    @staticmethod
    def relative_reconstruction_error(A: np.ndarray, A_approx: np.ndarray) -> float:
        A = np.asarray(A, dtype=float)
        A_approx = np.asarray(A_approx, dtype=float)
        norm_a = np.linalg.norm(A, ord="fro")
        if norm_a == 0:
            return 0.0
        return float(np.linalg.norm(A - A_approx, ord="fro") / norm_a)
