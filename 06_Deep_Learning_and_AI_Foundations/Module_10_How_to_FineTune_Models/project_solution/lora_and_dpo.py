"""Production solution for LoRALinear and DPOLossEvaluator."""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class LoRALinear(nn.Module):
    """Linear layer augmented with Low-Rank Adaptation (LoRA) parameter matrices."""

    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 8.0):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.scaling = alpha / rank

        # Freeze base linear layer
        self.base_layer = nn.Linear(in_features, out_features, bias=False)
        self.base_layer.weight.requires_grad = False

        # Trainable low-rank adapter matrices
        self.lora_A = nn.Parameter(torch.empty(rank, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))

        # Initialize A with Kaiming uniform and B with zeros
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        nn.init.zeros_(self.lora_B)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base_out = self.base_layer(x)
        # x: (..., in_features)
        # lora_out: x @ A^T @ B^T
        lora_out = (x @ self.lora_A.T) @ self.lora_B.T
        return base_out + self.scaling * lora_out


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
        pi_log_ratio = policy_chosen_logps - policy_rejected_logps
        ref_log_ratio = reference_chosen_logps - reference_rejected_logps
        logits = beta * (pi_log_ratio - ref_log_ratio)
        # Loss: -log(sigmoid(logits)) = log(1 + exp(-logits))
        losses = -F.logsigmoid(logits)
        return losses.mean()
