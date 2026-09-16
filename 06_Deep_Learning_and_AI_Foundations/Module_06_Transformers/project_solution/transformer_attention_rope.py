"""Production solution for Transformer Attention and RoPE."""
from __future__ import annotations

import math

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
        d_k = q.size(-1)
        # (batch, seq_q, seq_k)
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)

        if causal_mask:
            seq_len_q = q.size(-2)
            seq_len_k = k.size(-2)
            mask = torch.triu(
                torch.full((seq_len_q, seq_len_k), float("-inf"), device=q.device),
                diagonal=1,
            )
            scores = scores + mask

        attn_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, v)
        return output, attn_weights

    @staticmethod
    def apply_rope(x: torch.Tensor, seq_dim: int = 1) -> torch.Tensor:
        # x has shape (batch, seq_len, dim)
        _batch, seq_len, dim = x.shape
        assert dim % 2 == 0, "Dimension must be even for 2D complex pairing in RoPE."

        # Compute frequencies: theta_i = 10000^(-2(i-1)/dim)
        half_dim = dim // 2
        powers = (
            torch.arange(0, half_dim, dtype=torch.float32, device=x.device) / half_dim
        )
        inv_freq = 1.0 / (10000.0**powers)
        positions = torch.arange(seq_len, dtype=torch.float32, device=x.device)
        # Outer product: (seq_len, half_dim)
        sinusoids = torch.outer(positions, inv_freq)
        sin = torch.sin(sinusoids)
        cos = torch.cos(sinusoids)

        # Split x into pairs (x1, x2)
        x1 = x[..., :half_dim]
        x2 = x[..., half_dim:]

        # Rotate: (x1*cos - x2*sin, x1*sin + x2*cos)
        rot_1 = x1 * cos - x2 * sin
        rot_2 = x1 * sin + x2 * cos
        return torch.cat([rot_1, rot_2], dim=-1)
