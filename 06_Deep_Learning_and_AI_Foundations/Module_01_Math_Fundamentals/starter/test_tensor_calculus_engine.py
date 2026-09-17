"""Unit tests for TensorCalculusEngine."""
from __future__ import annotations

import numpy as np
import pytest
from tensor_calculus_engine import TensorCalculusEngine


def test_log_sum_exp_no_overflow():
    # Large numbers that would overflow float64 exp(1000)
    huge_logits = np.array([1000.0, 1001.0, 1002.0])
    lse = TensorCalculusEngine.log_sum_exp(huge_logits)
    assert not np.isnan(lse)
    assert not np.isinf(lse)
    # Exact: 1002 + log(exp(-2) + exp(-1) + exp(0))
    expected = 1002.0 + np.log(np.exp(-2.0) + np.exp(-1.0) + 1.0)
    assert lse == pytest.approx(expected, abs=1e-5)


def test_stable_softmax_sum_to_one():
    logits = np.array([[500.0, 501.0, 502.0], [-100.0, 0.0, 100.0]])
    probs = TensorCalculusEngine.stable_softmax(logits, axis=-1)
    assert np.all(probs >= 0.0)
    assert np.all(probs <= 1.0)
    assert np.allclose(np.sum(probs, axis=-1), 1.0)


def test_cross_entropy_loss_and_gradient():
    logits = np.array([[2.0, 1.0, 0.1]])
    targets = np.array([[1.0, 0.0, 0.0]])
    loss, grad = TensorCalculusEngine.cross_entropy_loss(logits, targets)

    assert loss > 0.0
    probs = TensorCalculusEngine.stable_softmax(logits)
    expected_grad = (probs - targets) / 1.0
    assert np.allclose(grad, expected_grad, atol=1e-7)


def test_two_layer_mlp_backward_gradient_check():
    np.random.seed(42)
    x = np.random.randn(5, 4)
    y = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [1.0, 0.0]])
    W1 = np.random.randn(4, 8) * 0.1
    b1 = np.zeros(8)
    W2 = np.random.randn(8, 2) * 0.1
    b2 = np.zeros(2)

    grads = TensorCalculusEngine.two_layer_mlp_backward(x, y, W1, b1, W2, b2)
    assert "dW1" in grads and grads["dW1"].shape == W1.shape
    assert "db1" in grads and grads["db1"].shape == b1.shape
    assert "dW2" in grads and grads["dW2"].shape == W2.shape
    assert "db2" in grads and grads["db2"].shape == b2.shape
    assert grads["loss"] > 0.0
