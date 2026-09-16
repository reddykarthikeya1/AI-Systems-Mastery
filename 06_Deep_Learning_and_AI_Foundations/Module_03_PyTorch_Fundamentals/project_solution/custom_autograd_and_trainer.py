"""Production solution for CustomGELU and ModelTrainer."""
from __future__ import annotations

import math

import torch
import torch.nn as nn


class CustomGELUFunction(torch.autograd.Function):
    """Custom numerically stable Gaussian Error Linear Unit (GELU) autograd function."""

    @staticmethod
    def forward(ctx, x: torch.Tensor) -> torch.Tensor:
        # Save input for backward pass
        ctx.save_for_backward(x)
        c = math.sqrt(2.0 / math.pi)
        inner = c * (x + 0.044715 * torch.pow(x, 3))
        tanh_inner = torch.tanh(inner)
        ctx.tanh_inner = tanh_inner
        return 0.5 * x * (1.0 + tanh_inner)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> torch.Tensor:
        (x,) = ctx.saved_tensors
        tanh_inner = ctx.tanh_inner
        c = math.sqrt(2.0 / math.pi)

        # d/dx [0.5 * x * (1 + tanh(inner))]
        # = 0.5 * (1 + tanh(inner)) + 0.5 * x * (1 - tanh^2(inner)) * c * (1 + 3 * 0.044715 * x^2)
        sech_sq = 1.0 - torch.pow(tanh_inner, 2)
        d_inner = c * (1.0 + 3.0 * 0.044715 * torch.pow(x, 2))
        dx = 0.5 * (1.0 + tanh_inner) + 0.5 * x * sech_sq * d_inner
        return grad_output * dx


def custom_gelu(x: torch.Tensor) -> torch.Tensor:
    return CustomGELUFunction.apply(x)


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
        model.train()
        optimizer.zero_grad()

        predictions = model(x)
        criterion = nn.MSELoss()
        loss = criterion(predictions, y)

        loss.backward()
        # Gradient clipping prevents exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_grad_norm)
        optimizer.step()

        return float(loss.item())
