"""Unit tests for TransformerAttention and RoPE."""
from __future__ import annotations

import torch
from transformer_attention_rope import TransformerAttention


def test_scaled_dot_product_attention_causal():
    batch, seq_len, d_k = 2, 4, 8
    q = torch.randn(batch, seq_len, d_k)
    k = torch.randn(batch, seq_len, d_k)
    v = torch.randn(batch, seq_len, d_k)

    out, weights = TransformerAttention.scaled_dot_product_attention(q, k, v, causal_mask=True)
    assert out.shape == (batch, seq_len, d_k)
    assert weights.shape == (batch, seq_len, seq_len)

    # Causal check: Upper triangle of attention matrix must be strictly 0.0
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            assert torch.all(weights[:, i, j] == 0.0)


def test_rope_rotation_invariance():
    batch, seq_len, dim = 1, 6, 8
    x = torch.randn(batch, seq_len, dim)
    x_rotated = TransformerAttention.apply_rope(x)

    assert x_rotated.shape == x.shape
    # Position 0 should have zero angle rotation (cos(0) = 1, sin(0) = 0)
    assert torch.allclose(x_rotated[:, 0, :], x[:, 0, :], atol=1e-5)
