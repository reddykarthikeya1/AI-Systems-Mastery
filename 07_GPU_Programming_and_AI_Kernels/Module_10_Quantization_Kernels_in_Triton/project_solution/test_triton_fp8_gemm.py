"""Unit tests for FP8 Matrix Multiplication Simulator."""

from __future__ import annotations

import numpy as np
from triton_fp8_gemm import FP8GemmSimulator


def test_fp8_e4m3_precision():
    np.random.seed(42)
    a = np.random.randn(16, 32).astype(np.float32)
    b = np.random.randn(32, 16).astype(np.float32)

    ref_c = a @ b
    fp8_c = FP8GemmSimulator.matmul_fp8(a, b, scale_a=10.0, scale_b=10.0, format_type="e4m3")

    rel_error = np.linalg.norm(ref_c - fp8_c) / np.linalg.norm(ref_c)
    assert rel_error < 0.20


def test_fp8_e5m2_dynamic_range():
    a = np.array([[1000.0, -2000.0]], dtype=np.float32)
    q = FP8GemmSimulator.quantize_fp8_e5m2(a, scale=1.0)
    assert not np.isnan(q).any()
    assert np.allclose(q, a, rtol=0.20)
