"""Unit tests for Quantization GEMM Engine."""
from __future__ import annotations

import numpy as np
import pytest
from quantization_gemm_engine import (
    dequantize_weights,
    pack_int4_weights,
    quantized_matmul_sim,
    unpack_int4_weights,
)


def test_pack_and_unpack_int4() -> None:
    original = np.array([3, 14, 0, 7, 15, 1, 9, 12], dtype=np.uint8)
    packed = pack_int4_weights(original)

    # 8 elements -> 4 packed uint8 bytes
    assert packed.size == 4
    assert packed[0] == (3 | (14 << 4))

    unpacked = unpack_int4_weights(packed, original_size=len(original))
    np.testing.assert_array_equal(unpacked, original)


def test_dequantize_group_scaling() -> None:
    # 256 weights with group_size=128 -> 2 groups
    raw_int4 = np.full(256, 8, dtype=np.uint8)
    packed = pack_int4_weights(raw_int4)

    scales = np.array([0.5, 0.25], dtype=np.float32)
    zeros = np.array([0.0, 0.0], dtype=np.float32)

    dequant = dequantize_weights(packed, scales, zeros, group_size=128, original_size=256)

    # Group 0: (8 - 0) * 0.5 = 4.0
    # Group 1: (8 - 0) * 0.25 = 2.0
    assert pytest.approx(float(dequant[0]), rel=1e-5) == 4.0
    assert pytest.approx(float(dequant[128]), rel=1e-5) == 2.0


def test_quantized_matmul_correctness() -> None:
    rng = np.random.default_rng(42)
    b, k, n = 2, 64, 4
    act = rng.standard_normal((b, k)).astype(np.float32)

    # Synthetic quantized weights
    w_int = rng.integers(0, 16, size=(n, k), dtype=np.uint8)
    packed_w = np.empty((n, k // 2), dtype=np.uint8)
    for i in range(n):
        packed_w[i] = pack_int4_weights(w_int[i])

    scales = np.full((n, 1), 0.1, dtype=np.float32)
    zeros = np.zeros((n, 1), dtype=np.float32)

    out_sim = quantized_matmul_sim(act, packed_w, scales, zeros, group_size=64)

    # Expected reference float matmul
    w_expected = w_int.astype(np.float32) * 0.1
    expected_out = act @ w_expected.T

    np.testing.assert_allclose(out_sim, expected_out, atol=1e-4)
