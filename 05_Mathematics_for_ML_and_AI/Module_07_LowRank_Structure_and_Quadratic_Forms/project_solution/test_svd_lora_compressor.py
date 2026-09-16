"""Unit tests for SVDLoRACompressor."""
from __future__ import annotations

import numpy as np
import pytest
from svd_lora_compressor import SVDLoRACompressor


def test_svd_truncation_and_error():
    # Construct rank 2 matrix in 4x3 space
    np.random.seed(42)
    u = np.random.randn(4, 2)
    v = np.random.randn(2, 3)
    rank2_mat = u @ v

    u_k, s_k, vh_k = SVDLoRACompressor.truncate_svd(rank2_mat, rank=2)
    reconstructed = u_k @ np.diag(s_k) @ vh_k

    rel_error = SVDLoRACompressor.relative_reconstruction_error(rank2_mat, reconstructed)
    assert rel_error < 1e-10
    assert len(s_k) == 2


def test_energy_retention():
    singular_values = np.array([10.0, 5.0, 1.0])
    # Total energy: 100 + 25 + 1 = 126
    # Rank 1 energy: 100 / 126 = 0.79365
    retention_1 = SVDLoRACompressor.energy_retention(singular_values, rank=1)
    retention_2 = SVDLoRACompressor.energy_retention(singular_values, rank=2)
    assert retention_1 == pytest.approx(100.0 / 126.0, rel=1e-4)
    assert retention_2 == pytest.approx(125.0 / 126.0, rel=1e-4)


def test_lora_factorization():
    W = np.random.randn(20, 10)
    rank = 3
    B, A = SVDLoRACompressor.lora_factorize(W, rank=rank)
    assert B.shape == (20, rank)
    assert A.shape == (rank, 10)

    W_approx = B @ A
    assert W_approx.shape == W.shape
    # Reconstruction with rank 3 must retain significant portion of W
    rel_error = SVDLoRACompressor.relative_reconstruction_error(W, W_approx)
    assert rel_error < 1.0


def test_positive_definite_check():
    # Identity matrix is positive definite
    I3 = np.eye(3)
    assert SVDLoRACompressor.is_positive_definite(I3)

    # Matrix with negative eigenvalue is not positive definite
    saddle_mat = np.array([[2.0, 0.0], [0.0, -1.0]])
    assert not SVDLoRACompressor.is_positive_definite(saddle_mat)

    # Non-symmetric matrix is not positive definite by definition
    non_sym = np.array([[2.0, 3.0], [1.0, 2.0]])
    assert not SVDLoRACompressor.is_positive_definite(non_sym)
