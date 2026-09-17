"""Tests for Shared Memory Gemm Tiling."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_shared_memory_gemm_tiling import shared_memory_gemm_tiling
except ImportError:
    from p01_shared_memory_gemm_tiling import shared_memory_gemm_tiling


def test_shared_memory_gemm_tiling():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    C = shared_memory_gemm_tiling(A, B)
    # C[0][0] = 1*5 + 2*7 = 19
    assert C[0][0] == 19.0
