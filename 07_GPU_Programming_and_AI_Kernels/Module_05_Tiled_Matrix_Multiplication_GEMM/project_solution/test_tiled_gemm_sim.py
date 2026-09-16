"""Unit tests for Tiled GEMM Simulator."""
from __future__ import annotations

import numpy as np
import pytest
from tiled_gemm_sim import (
    calculate_gemm_arithmetic_intensity,
    tiled_gemm_2d,
)


def test_tiled_gemm_correctness() -> None:
    rng = np.random.default_rng(42)
    a = rng.standard_normal((32, 24))
    b = rng.standard_normal((24, 40))

    c_sim, _, _ = tiled_gemm_2d(a, b, tile_size=8)
    c_expected = a @ b

    np.testing.assert_allclose(c_sim, c_expected, atol=1e-5)


def test_tiled_memory_reduction() -> None:
    # 32x32 matrices with tile_size=16
    a = np.ones((32, 32), dtype=np.float64)
    b = np.ones((32, 32), dtype=np.float64)

    _, global_reads, shared_reads = tiled_gemm_2d(a, b, tile_size=16)

    # In naive GEMM, each element of C (1024 elements) reads 32 elements of A and 32 of B
    naive_reads = 1024 * 64  # 65,536 reads
    # With tiling, global reads should be dramatically smaller than naive reads
    assert global_reads < naive_reads
    assert shared_reads > global_reads


def test_arithmetic_intensity_boost() -> None:
    m = n = k = 1024
    naive_i, tiled_i = calculate_gemm_arithmetic_intensity(m, n, k, tile_size=32)
    # Tiled intensity must be significantly higher than naive intensity
    assert tiled_i > naive_i
    assert pytest.approx(tiled_i / naive_i, rel=0.1) == 32.0
