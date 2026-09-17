from __future__ import annotations

import numpy as np
import pytest
from ring_attention_sim import RingAttentionSimulator


def test_ring_attention_non_causal_equivalence():
    np.random.seed(42)
    seq_len, d, ranks = 64, 16, 4
    sim = RingAttentionSimulator(seq_len=seq_len, head_dim=d, num_ranks=ranks, causal=False)

    q = np.random.randn(seq_len, d).astype(np.float32)
    k = np.random.randn(seq_len, d).astype(np.float32)
    v = np.random.randn(seq_len, d).astype(np.float32)

    ref_out = sim.run_monolithic_reference(q, k, v)
    ring_out = sim.run_ring_attention(q, k, v)

    np.testing.assert_allclose(ring_out, ref_out, rtol=1e-5, atol=1e-5)


def test_ring_attention_causal_equivalence():
    np.random.seed(42)
    seq_len, d, ranks = 64, 16, 4
    sim = RingAttentionSimulator(seq_len=seq_len, head_dim=d, num_ranks=ranks, causal=True)

    q = np.random.randn(seq_len, d).astype(np.float32)
    k = np.random.randn(seq_len, d).astype(np.float32)
    v = np.random.randn(seq_len, d).astype(np.float32)

    ref_out = sim.run_monolithic_reference(q, k, v)
    ring_out = sim.run_ring_attention(q, k, v)

    np.testing.assert_allclose(ring_out, ref_out, rtol=1e-4, atol=1e-4)


def test_ring_attention_divisibility():
    with pytest.raises(ValueError, match="divisible by num_ranks"):
        RingAttentionSimulator(seq_len=30, head_dim=16, num_ranks=4)
