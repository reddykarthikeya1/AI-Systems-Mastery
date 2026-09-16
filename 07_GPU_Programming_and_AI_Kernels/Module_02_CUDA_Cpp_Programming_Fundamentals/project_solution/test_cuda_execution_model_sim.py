"""Unit tests for CUDA Execution Model Simulator."""
from __future__ import annotations

import numpy as np
from cuda_execution_model_sim import (
    compute_1d_index,
    compute_2d_coords,
    matrix_transpose_naive,
    vector_add_grid_stride,
)


def test_1d_and_2d_indexing() -> None:
    # 1D index: block 3, block_dim 128, thread 42 -> 3 * 128 + 42 = 426
    idx = compute_1d_index(3, 128, 42)
    assert idx == 426

    # 2D coords: block (2, 3), block_dim (16, 16), thread (5, 7), width 128
    # col = 2 * 16 + 5 = 37
    # row = 3 * 16 + 7 = 55
    # linear_idx = 55 * 128 + 37 = 7077
    row, col, linear = compute_2d_coords((2, 3), (16, 16), (5, 7), 128)
    assert (row, col, linear) == (55, 37, 7077)


def test_vector_add_grid_stride() -> None:
    n = 1000
    a = np.arange(n, dtype=np.float32)
    b = np.full(n, 2.5, dtype=np.float32)

    # Grid smaller than N: requires multiple grid-stride iterations
    c = vector_add_grid_stride(a, b, grid_dim=4, block_dim=64)
    expected = a + b
    np.testing.assert_allclose(c, expected)


def test_matrix_transpose_2d() -> None:
    mat = np.arange(24, dtype=np.float32).reshape(4, 6)
    transposed = matrix_transpose_naive(mat, block_dim=(4, 4))
    np.testing.assert_allclose(transposed, mat.T)
