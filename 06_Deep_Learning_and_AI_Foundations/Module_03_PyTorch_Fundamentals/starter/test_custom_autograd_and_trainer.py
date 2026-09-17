"""Unit tests for CustomGELU and ModelTrainer."""
from __future__ import annotations

import torch
import torch.nn as nn
from custom_autograd_and_trainer import CustomGELUFunction, ModelTrainer


def test_custom_gelu_forward_and_backward():
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=torch.float64, requires_grad=True)
    # Compare with PyTorch's native approximate GELU
    native_gelu = nn.GELU(approximate="tanh")
    x_native = x.clone().detach().requires_grad_(True)

    y_custom = CustomGELUFunction.apply(x)
    y_native = native_gelu(x_native)
    assert torch.allclose(y_custom, y_native, atol=1e-5)

    y_custom.sum().backward()
    y_native.sum().backward()
    assert torch.allclose(x.grad, x_native.grad, atol=1e-5)


def test_model_trainer_step():
    torch.manual_seed(42)
    # Simple linear regression model
    model = nn.Linear(4, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

    x = torch.randn(10, 4)
    y = torch.randn(10, 1)

    loss_1 = ModelTrainer.train_step(model, optimizer, x, y, max_grad_norm=1.0)
    loss_2 = ModelTrainer.train_step(model, optimizer, x, y, max_grad_norm=1.0)

    assert isinstance(loss_1, float)
    assert loss_1 > 0.0
    # Training step should decrease or maintain loss
    assert loss_2 <= loss_1 + 0.1
