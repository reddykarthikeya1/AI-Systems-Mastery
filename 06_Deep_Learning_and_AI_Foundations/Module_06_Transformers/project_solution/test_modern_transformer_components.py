"""Unit tests for Modern Transformer Components (RoPE, SwiGLU, RMSNorm)."""

from __future__ import annotations

import numpy as np
import pytest
from modern_transformer_components import RMSNorm, RotaryPositionEmbedding, SwiGLU


def test_rmsnorm_invariants():
    norm = RMSNorm(d_model=64)
    x = np.random.randn(2, 10, 64).astype(np.float32) * 5.0
    out = norm.forward(x)

    out_rms = np.sqrt(np.mean(out * out, axis=-1))
    assert np.allclose(out_rms, 1.0, atol=1e-3)


def test_swiglu_output_shape():
    batch, seq, d_in, d_ff = 2, 4, 32, 64
    x = np.random.randn(batch, seq, d_in).astype(np.float32)
    w_gate = np.random.randn(d_in, d_ff).astype(np.float32)
    w_up = np.random.randn(d_in, d_ff).astype(np.float32)
    w_down = np.random.randn(d_ff, d_in).astype(np.float32)

    out = SwiGLU.forward(x, w_gate, w_up, w_down)
    assert out.shape == (batch, seq, d_in)


def test_rope_relative_distance_rotation():
    rope = RotaryPositionEmbedding(d_head=16)
    x = np.ones((1, 4, 1, 16), dtype=np.float32)
    rotated = rope.apply_rope(x, seq_len=4)

    # Position 0 has angle 0, so cos=1, sin=0 -> unchanged
    assert np.allclose(rotated[:, 0, :, :], 1.0, atol=1e-5)

    # Subsequent positions are rotated
    assert not np.allclose(rotated[:, 1, :, :], 1.0, atol=1e-3)

    # Relative dot product test
    q = rotated[:, 1, 0, :]
    k = rotated[:, 3, 0, :]
    dot_dist_2 = np.dot(q.flatten(), k.flatten())

    q2 = rotated[:, 0, 0, :]
    k2 = rotated[:, 2, 0, :]
    dot_dist_2_prime = np.dot(q2.flatten(), k2.flatten())

    assert pytest.approx(float(dot_dist_2), rel=0.05) == float(dot_dist_2_prime)
