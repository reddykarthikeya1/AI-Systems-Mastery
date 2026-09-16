"""Production solution for SparseMoERouter."""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class SparseMoERouter(nn.Module):
    """Top-k sparse expert router with auxiliary load balancing loss."""

    def __init__(self, d_model: int, num_experts: int = 8, top_k: int = 2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, num_experts, bias=False)

    def forward(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # x shape: (batch, seq_len, d_model) -> flatten to (N, d_model)
        orig_shape = x.shape
        x_flat = x.view(-1, self.d_model)

        # Raw gate logits
        logits = self.gate(x_flat)
        # Softmax over all experts
        gate_probs = F.softmax(logits, dim=-1)

        # Select Top-K experts
        topk_weights, topk_indices = torch.topk(gate_probs, self.top_k, dim=-1)
        # Renormalize top-k weights so they sum to 1.0 per token
        topk_weights = topk_weights / topk_weights.sum(dim=-1, keepdim=True)

        # Auxiliary Load Balancing Loss: num_experts * sum_i(f_i * P_i)
        # f_i = fraction of tokens routed to expert i
        # P_i = average probability assigned to expert i
        me = gate_probs.mean(dim=0)  # P_i
        # Count token assignments to expert i
        mask = F.one_hot(topk_indices, self.num_experts).sum(dim=1)  # (N, num_experts)
        ce = mask.float().mean(dim=0)  # f_i
        aux_loss = self.num_experts * torch.sum(me * ce)

        # Reshape topk outputs back to batch dimensions
        out_weights = topk_weights.view(*orig_shape[:-1], self.top_k)
        out_indices = topk_indices.view(*orig_shape[:-1], self.top_k)

        return out_weights, out_indices, aux_loss
