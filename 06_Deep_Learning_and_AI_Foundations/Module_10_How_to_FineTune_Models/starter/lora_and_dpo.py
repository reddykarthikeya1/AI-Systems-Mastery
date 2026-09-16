"""Starter template for LoRALinear and DPOLossEvaluator."""
from __future__ import annotations

import torch
import torch.nn as nn


class LoRALinear(nn.Module):
    """Linear layer augmented with Low-Rank Adaptation (LoRA) parameter matrices."""

    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 8.0):
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Compute y = x @ W_base^T + (alpha / rank) * (x @ A^T @ B^T)."""
        raise NotImplementedError


class DPOLossEvaluator:
    """Direct Preference Optimization (DPO) loss calculator."""

    @staticmethod
    def compute_dpo_loss(
        policy_chosen_logps: torch.Tensor,
        policy_rejected_logps: torch.Tensor,
        reference_chosen_logps: torch.Tensor,
        reference_rejected_logps: torch.Tensor,
        beta: float = 0.1,
    ) -> torch.Tensor:
        """Compute DPO loss: -log(sigmoid(beta * (log_ratio_w - log_ratio_l)))."""
        raise NotImplementedError
