"""Unit tests for SparseMoERouter."""
from __future__ import annotations

import torch
from moe_sparse_router import SparseMoERouter


def test_sparse_moe_router_shapes_and_normalization():
    torch.manual_seed(42)
    batch, seq_len, d_model = 2, 4, 16
    num_experts, top_k = 4, 2
    router = SparseMoERouter(d_model=d_model, num_experts=num_experts, top_k=top_k)

    x = torch.randn(batch, seq_len, d_model)
    weights, indices, aux_loss = router(x)

    assert weights.shape == (batch, seq_len, top_k)
    assert indices.shape == (batch, seq_len, top_k)
    # Weights must sum to 1.0 across selected top-k
    assert torch.allclose(weights.sum(dim=-1), torch.ones(batch, seq_len))
    # Indices must be within [0, num_experts - 1]
    assert torch.all(indices >= 0) and torch.all(indices < num_experts)
    # Aux loss must be a positive scalar
    assert aux_loss.item() > 0.0
