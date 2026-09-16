"""Starter template for GramSchmidtQR."""
from __future__ import annotations

import numpy as np


class GramSchmidtQR:
    """Orthonormalization and QR decomposition."""

    @staticmethod
    def qr_factorization(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Compute QR factorization A = Q @ R using Gram-Schmidt."""
        raise NotImplementedError

    @staticmethod
    def project_onto_subspace(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Compute the orthogonal projection of vector b onto the column space of A."""
        raise NotImplementedError
