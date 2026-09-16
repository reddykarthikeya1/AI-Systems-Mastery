"""Production reference implementation for CUDA Execution Model Simulator."""
from __future__ import annotations

import numpy as np


def compute_1d_index(block_idx: int, block_dim: int, thread_idx: int) -> int:
    """Calculate 1D global thread index.

    Formula: idx = blockIdx.x * blockDim.x + threadIdx.x
    """
    if thread_idx < 0 or thread_idx >= block_dim:
        raise ValueError("thread_idx must be within [0, block_dim - 1].")
    return block_idx * block_dim + thread_idx


def compute_2d_coords(
    block_idx: tuple[int, int],
    block_dim: tuple[int, int],
    thread_idx: tuple[int, int],
    width: int,
) -> tuple[int, int, int]:
    """Calculate (row, col, linear_idx) in row-major 2D matrix.

    Row = blockIdx.y * blockDim.y + threadIdx.y
    Col = blockIdx.x * blockDim.x + threadIdx.x
    linear_idx = Row * width + Col
    """
    b_x, b_y = block_idx
    d_x, d_y = block_dim
    t_x, t_y = thread_idx

    col = b_x * d_x + t_x
    row = b_y * d_y + t_y
    linear_idx = row * width + col
    return row, col, linear_idx


def vector_add_grid_stride(
    a: np.ndarray, b: np.ndarray, grid_dim: int, block_dim: int
) -> np.ndarray:
    """Simulate parallel vector addition using grid-stride loops.

    In a CUDA grid-stride loop, total threads in the grid = grid_dim * block_dim.
    Each thread starts at its global ID and strides by the grid size until N.
    """
    if a.shape != b.shape:
        raise ValueError("Arrays a and b must have matching shapes.")

    n = a.size
    c = np.zeros_like(a)
    stride = grid_dim * block_dim

    # Simulate thread executions in parallel
    for b_idx in range(grid_dim):
        for t_idx in range(block_dim):
            global_id = b_idx * block_dim + t_idx
            # Grid-stride loop
            curr = global_id
            while curr < n:
                c[curr] = a[curr] + b[curr]
                curr += stride

    return c


def matrix_transpose_naive(
    matrix: np.ndarray, block_dim: tuple[int, int] = (16, 16)
) -> np.ndarray:
    """Simulate 2D grid kernel matrix transpose.

    Input shape: (H, W) -> Output shape: (W, H).
    """
    h, w = matrix.shape
    out = np.zeros((w, h), dtype=matrix.dtype)

    b_dim_x, b_dim_y = block_dim
    grid_x = (w + b_dim_x - 1) // b_dim_x
    grid_y = (h + b_dim_y - 1) // b_dim_y

    for gy in range(grid_y):
        for gx in range(grid_x):
            for ty in range(b_dim_y):
                for tx in range(b_dim_x):
                    row, col, _ = compute_2d_coords((gx, gy), (b_dim_x, b_dim_y), (tx, ty), w)
                    if row < h and col < w:
                        out[col, row] = matrix[row, col]

    return out
