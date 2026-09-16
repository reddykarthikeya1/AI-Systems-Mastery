"""Starter template for Transformer Attention and RoPE."""
from __future__ import annotations

import torch


class TransformerAttention:
    """Scaled dot-product attention, causal masking, and rotary position embeddings."""

    @staticmethod
    def scaled_dot_product_attention(
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        causal_mask: bool = False,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute Softmax((Q @ K.T) / sqrt(d_k) + mask) @ V."""
        raise NotImplementedError

    @staticmethod
    def apply_rope(x: torch.Tensor, seq_dim: int = 1) -> torch.Tensor:
        """Apply Rotary Position Embeddings (RoPE) to token representations."""
        raise NotImplementedError
