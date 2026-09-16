"""Unit tests for Fused Normalization and Activations Engine."""
from __future__ import annotations

import numpy as np
from fused_norm_and_activations import (
    fused_rmsnorm,
    fused_swiglu,
    online_safe_softmax_step,
)


def test_fused_rmsnorm_correctness() -> None:
    rng = np.random.default_rng(42)
    x = rng.standard_normal((4, 16, 64), dtype=np.float64)
    weight = rng.standard_normal(64, dtype=np.float64)

    out = fused_rmsnorm(x, weight, eps=1e-5)

    # Validate against direct formula
    expected_rms = np.sqrt(np.mean(x ** 2, axis=-1, keepdims=True) + 1e-5)
    expected = (x / expected_rms) * weight
    np.testing.assert_allclose(out, expected, atol=1e-6)


def test_fused_swiglu_correctness() -> None:
    gate = np.array([-2.0, 0.0, 3.0], dtype=np.float64)
    up = np.array([1.5, 2.0, -1.0], dtype=np.float64)

    out = fused_swiglu(gate, up)

    # Reference Swish
    sig = 1.0 / (1.0 + np.exp(-gate))
    expected = (gate * sig) * up
    np.testing.assert_allclose(out, expected, atol=1e-6)


def test_online_safe_softmax_equivalence() -> None:
    # Full sequence of 8 numbers split into two blocks of 4
    x = np.array([1.0, 4.0, 2.0, 5.0, 3.0, 7.0, 2.0, 6.0], dtype=np.float64)
    v = np.array([0.5, 1.2, -0.3, 2.1, 1.0, -1.5, 0.8, 3.0], dtype=np.float64)

    scores1, val1 = x[:4], v[:4]
    scores2, val2 = x[4:], v[4:]

    # Pass 1: block 1
    m1 = float(np.max(scores1))
    p1 = np.exp(scores1 - m1)
    l1 = float(np.sum(p1))
    acc1 = np.dot(p1, val1)

    # Pass 2: online update with block 2
    _, l2, acc2 = online_safe_softmax_step(m1, l1, acc1, scores2, val2)

    # Final attention output
    out_online = acc2 / l2

    # Global standard attention output
    exp_global = np.exp(x - np.max(x))
    attn_weights = exp_global / np.sum(exp_global)
    expected_out = np.dot(attn_weights, v)

    np.testing.assert_allclose(out_online, expected_out, atol=1e-6)
