"""Unit tests for FlashAttention Engine."""
from __future__ import annotations

import numpy as np
from flash_attention_engine import flash_attention_forward


def test_flash_attention_matches_standard() -> None:
    rng = np.random.default_rng(42)
    n, d = 64, 32
    q = rng.standard_normal((n, d))
    k = rng.standard_normal((n, d))
    v = rng.standard_normal((n, d))

    # FlashAttention with small blocks (16x16)
    out_fa, reads, writes = flash_attention_forward(q, k, v, block_r=16, block_c=16)

    # Standard attention: softmax(Q @ K.T / sqrt(d)) @ V
    scale = 1.0 / np.sqrt(d)
    scores = (q @ k.T) * scale
    exp_scores = np.exp(scores - np.max(scores, axis=1, keepdims=True))
    attn_probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    out_expected = attn_probs @ v

    np.testing.assert_allclose(out_fa, out_expected, atol=1e-5)


def test_flash_attention_io_advantage() -> None:
    n, d = 128, 32
    q = np.ones((n, d))
    k = np.ones((n, d))
    v = np.ones((n, d))

    _, reads, writes = flash_attention_forward(q, k, v, block_r=32, block_c=32)

    # Standard attention must write N x N (16,384 floats) and read N x N
    standard_matrix_io = n * n * 2  # writes + reads of attention matrix

    # Verify that FlashAttention never writes an N x N matrix to HBM
    # Output writes are strictly N x d (128 x 32 = 4,096 floats)
    assert writes == n * d
    assert writes < standard_matrix_io
