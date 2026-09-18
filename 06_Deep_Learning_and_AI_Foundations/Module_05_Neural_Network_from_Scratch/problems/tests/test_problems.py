"""Tests for Two Layer Mlp Backward."""
from __future__ import annotations

import pytest
from p01_two_layer_mlp_backward import two_layer_mlp_backward


def test_two_layer_mlp_backward():
    gw1, gw2 = two_layer_mlp_backward(2.0, 4.0, 1.0, 1.0)
    # z1 = 2, h = 2, y_hat = 2. dloss = -2. grad_w2 = -4. grad_w1 = -4 * 1 * 2 = -4.
    assert gw1 == -4.0 and gw2 == -4.0
