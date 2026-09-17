"""Unit tests for Triton Block Execution Engine."""
from __future__ import annotations

import numpy as np
from triton_block_engine import (
    triton_block_softmax_sim,
    triton_masked_load,
    triton_masked_store,
    triton_vector_add_sim,
)


def test_triton_masked_load_and_store() -> None:
    data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    offsets = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    # Boundary is 5 elements. Offsets 5, 6, 7 should be filled with 0.0
    loaded = triton_masked_load(data, offsets, boundary=5, fill_value=0.0)
    expected_load = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 0.0, 0.0, 0.0])
    np.testing.assert_allclose(loaded, expected_load)

    # Store back into target array
    target = np.zeros(5)
    triton_masked_store(target, offsets, loaded * 2, boundary=5)
    np.testing.assert_allclose(target, np.array([20.0, 40.0, 60.0, 80.0, 100.0]))


def test_triton_vector_add_sim() -> None:
    x = np.linspace(0.0, 10.0, 250, dtype=np.float32)
    y = np.linspace(5.0, 15.0, 250, dtype=np.float32)
    result = triton_vector_add_sim(x, y, block_size=64)
    np.testing.assert_allclose(result, x + y)


def test_triton_block_softmax() -> None:
    rng = np.random.default_rng(123)
    x = rng.standard_normal((10, 45))
    probs = triton_block_softmax_sim(x, block_size=64)

    # Verify probability distribution properties
    row_sums = np.sum(probs, axis=1)
    np.testing.assert_allclose(row_sums, np.ones(10), atol=1e-5)
    assert np.all(probs >= 0.0)

    # Verify matching scipy/standard softmax
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    expected_softmax = exp_x / np.sum(exp_x, axis=1, keepdims=True)
    np.testing.assert_allclose(probs, expected_softmax, atol=1e-5)
