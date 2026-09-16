"""Unit tests for CausalAttentionKVCache."""
from __future__ import annotations

import torch
from nanogpt_kv_cache import CausalAttentionKVCache


def test_kv_cache_matches_full_context_generation():
    torch.manual_seed(42)
    d_model, n_heads = 16, 2
    model = CausalAttentionKVCache(d_model, n_heads)
    model.eval()

    # Sequence of 3 tokens
    full_seq = torch.randn(1, 3, d_model)

    # 1. Full context forward pass
    with torch.no_grad():
        full_out, _ = model(full_seq)

    # 2. Incremental generation with KV-cache
    with torch.no_grad():
        # Prefill first 2 tokens
        _, cache = model(full_seq[:, :2, :])
        # Generate 3rd token using cache
        token_3_input = full_seq[:, 2:3, :]
        cached_out_3, _ = model(token_3_input, past_kv=cache)

    # The output for token 3 must match identically
    assert torch.allclose(full_out[:, 2:3, :], cached_out_3, atol=1e-5)
