"""Tests for Gradient Descent Backtracking."""
from __future__ import annotations

import pytest
from p01_gradient_descent_backtracking import gradient_descent_backtracking


def test_gradient_descent_backtracking():
    loss = lambda x: x ** 2
    # At x=2, grad=4. Candidate with lr=1 -> x_new = -2 (loss 4 == 4 ok)
    # With small step, x drops toward 0
    x_next = gradient_descent_backtracking(2.0, 4.0, loss, lr=0.1)
    assert x_next == 1.6
