"""Starter template for SparseMoERouter."""
from __future__ import annotations

import torch
import torch.nn as nn


class SparseMoERouter(nn.Module):
    """Top-k sparse expert router with auxiliary load balancing loss."""

    def __init__(self, d_model: int, num_experts: int = 8, top_k: int = 2):
        super().__init__()
        raise NotImplementedError

    def forward(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Route tokens to top_k experts. Returns (weights, indices, aux_loss)."""
        raise NotImplementedError
