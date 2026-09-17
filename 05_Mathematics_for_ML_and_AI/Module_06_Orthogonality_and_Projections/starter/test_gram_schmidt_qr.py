"""Unit tests for GramSchmidtQR."""
from __future__ import annotations

import numpy as np
from gram_schmidt_qr import GramSchmidtQR


def test_qr_decomposition():
    A = np.array([
        [1.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 1.0],
    ])
    Q, R = GramSchmidtQR.qr_factorization(A)

    # Q must have orthonormal columns: Q.T @ Q = I
    assert np.allclose(Q.T @ Q, np.eye(3))
    # R must be upper-triangular
    assert np.allclose(np.tril(R, -1), 0.0)
    # A = Q @ R
    assert np.allclose(Q @ R, A)


def test_orthogonal_projection():
    # 2D XY plane in 3D space
    A = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
    ])
    # Vector hovering above XY plane
    b = np.array([3.0, 4.0, 5.0])
    proj = GramSchmidtQR.project_onto_subspace(A, b)

    # Shadow on XY plane must be [3, 4, 0]
    assert np.allclose(proj, [3.0, 4.0, 0.0])
