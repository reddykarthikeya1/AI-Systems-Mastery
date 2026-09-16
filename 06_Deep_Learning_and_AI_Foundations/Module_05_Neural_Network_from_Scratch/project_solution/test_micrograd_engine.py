"""Unit tests for Micrograd autograd engine."""
from __future__ import annotations

import pytest
import torch
from micrograd_engine import Value


def test_micrograd_matches_pytorch_gradients():
    # Micrograd computation
    a = Value(2.0)
    b = Value(-3.0)
    c = a * b
    d = c + 4.0
    e = d.relu()
    loss = e * 2.0
    loss.backward()

    # Exact PyTorch equivalent
    a_pt = torch.tensor(2.0, requires_grad=True, dtype=torch.float64)
    b_pt = torch.tensor(-3.0, requires_grad=True, dtype=torch.float64)
    c_pt = a_pt * b_pt
    d_pt = c_pt + 4.0
    e_pt = torch.relu(d_pt)
    loss_pt = e_pt * 2.0
    loss_pt.backward()

    # Verify forward value and exact gradients
    assert loss.data == pytest.approx(float(loss_pt.item()))
    assert a.grad == pytest.approx(float(a_pt.grad.item()))
    assert b.grad == pytest.approx(float(b_pt.grad.item()))


def test_micrograd_pow_and_sub():
    x = Value(3.0)
    y = (x - 1.0) ** 2
    y.backward()
    # dy/dx = 2 * (x - 1) = 2 * 2 = 4.0
    assert y.data == pytest.approx(4.0)
    assert x.grad == pytest.approx(4.0)
