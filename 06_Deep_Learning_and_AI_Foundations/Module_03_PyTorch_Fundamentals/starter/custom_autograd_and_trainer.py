"""Starter template for CustomGELU and ModelTrainer."""
from __future__ import annotations

import torch
import torch.nn as nn


class CustomGELUFunction(torch.autograd.Function):
    """Custom numerically stable Gaussian Error Linear Unit (GELU) autograd function."""

    @staticmethod
    def forward(ctx, x: torch.Tensor) -> torch.Tensor:
        """Compute GELU approximation: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))."""
        raise NotImplementedError

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> torch.Tensor:
        """Compute analytical gradient of GELU with respect to input x."""
        raise NotImplementedError


class ModelTrainer:
    """Production PyTorch training harness with gradient clipping and optimizer step."""

    @staticmethod
    def train_step(
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        x: torch.Tensor,
        y: torch.Tensor,
        max_grad_norm: float = 1.0,
    ) -> float:
        """Run single forward/backward training step with gradient clipping by norm."""
        raise NotImplementedError
