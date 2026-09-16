"""Starter template for CUDA Execution Model Simulator."""
from __future__ import annotations

import numpy as np


def compute_1d_index(block_idx: int, block_dim: int, thread_idx: int) -> int:
    """Calculate 1D global thread index."""
    raise NotImplementedError("Implement compute_1d_index")


def compute_2d_coords(
    block_idx: tuple[int, int],
    block_dim: tuple[int, int],
    thread_idx: tuple[int, int],
    width: int,
) -> tuple[int, int, int]:
    """Calculate (row, col, linear_idx) in row-major 2D matrix."""
    raise NotImplementedError("Implement compute_2d_coords")


def vector_add_grid_stride(
    a: np.ndarray, b: np.ndarray, grid_dim: int, block_dim: int
) -> np.ndarray:
    """Simulate parallel vector addition using grid-stride loops."""
    raise NotImplementedError("Implement vector_add_grid_stride")


def matrix_transpose_naive(matrix: np.ndarray, block_dim: tuple[int, int] = (16, 16)) -> np.ndarray:
    """Simulate 2D grid kernel matrix transpose."""
    raise NotImplementedError("Implement matrix_transpose_naive")
