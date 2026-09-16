"""Starter template for TensorCalculusEngine."""
from __future__ import annotations

import numpy as np


class TensorCalculusEngine:
    """Numerical stability tricks, Softmax, Cross-Entropy, and manual MLP backprop."""

    @staticmethod
    def log_sum_exp(x: np.ndarray, axis: int = -1, keepdims: bool = False) -> np.ndarray:
        """Compute log(sum(exp(x))) in a numerically stable way by subtracting max(x)."""
        raise NotImplementedError

    @staticmethod
    def stable_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Compute Softmax probabilities using the max subtraction stability trick."""
        raise NotImplementedError

    @staticmethod
    def cross_entropy_loss(
        logits: np.ndarray, targets: np.ndarray
    ) -> tuple[float, np.ndarray]:
        """Compute categorical cross-entropy loss and analytical gradient w.r.t logits (P - Y)."""
        raise NotImplementedError

    @staticmethod
    def two_layer_mlp_backward(
        x: np.ndarray,
        y: np.ndarray,
        W1: np.ndarray,
        b1: np.ndarray,
        W2: np.ndarray,
        b2: np.ndarray,
    ) -> dict[str, np.ndarray]:
        """Compute analytical gradients dW1, db1, dW2, db2 for 2-layer MLP with ReLU."""
        raise NotImplementedError
