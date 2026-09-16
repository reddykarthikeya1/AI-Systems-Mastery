"""Starter template for CausalSelfAttentionWithKVCache."""
from __future__ import annotations

import torch
import torch.nn as nn


class CausalAttentionKVCache(nn.Module):
    """Causal self-attention with step-by-step Key-Value caching."""

    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        raise NotImplementedError

    def forward(
        self,
        x: torch.Tensor,
        past_kv: tuple[torch.Tensor, torch.Tensor] | None = None,
    ) -> tuple[torch.Tensor, tuple[torch.Tensor, torch.Tensor]]:
        """Forward pass taking (batch, seq_len, d_model).
        Returns (output, (k_cache, v_cache)).
        """
        raise NotImplementedError
