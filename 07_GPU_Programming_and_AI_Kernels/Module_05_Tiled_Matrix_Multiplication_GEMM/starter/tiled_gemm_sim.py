"""Starter template for Tiled GEMM Simulator."""
from __future__ import annotations

import numpy as np


def calculate_gemm_arithmetic_intensity(
    m: int, n: int, k: int, tile_size: int, elem_bytes: int = 4
) -> tuple[float, float]:
    """Calculate arithmetic intensity for naive vs tiled GEMM."""
    raise NotImplementedError("Implement calculate_gemm_arithmetic_intensity")


def tiled_gemm_2d(
    a: np.ndarray, b: np.ndarray, tile_size: int = 16
) -> tuple[np.ndarray, int, int]:
    """Simulate 2D tiled GEMM, tracking global and shared memory reads.

    Returns:
        tuple of (c_matrix, global_memory_reads, shared_memory_reads).
    """
    raise NotImplementedError("Implement tiled_gemm_2d")
