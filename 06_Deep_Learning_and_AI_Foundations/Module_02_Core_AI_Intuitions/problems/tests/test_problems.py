"""Tests for Binary Cross Entropy Gradient."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_binary_cross_entropy_gradient import binary_cross_entropy_gradient
except ImportError:
    from p01_binary_cross_entropy_gradient import binary_cross_entropy_gradient


def test_binary_cross_entropy_gradient():
    loss, grad = binary_cross_entropy_gradient(1.0, 0.9)
    assert loss > 0
    assert grad < 0  # negative gradient to push prediction higher towards 1
