"""Production solution for TensorCalculusEngine."""
from __future__ import annotations

import numpy as np


class TensorCalculusEngine:
    """Numerical stability tricks, Softmax, Cross-Entropy, and manual MLP backprop."""

    @staticmethod
    def log_sum_exp(x: np.ndarray, axis: int = -1, keepdims: bool = False) -> np.ndarray:
        x_arr = np.asarray(x, dtype=float)
        max_val = np.max(x_arr, axis=axis, keepdims=True)
        # Avoid -inf when all values are -inf
        max_val_clipped = np.where(np.isneginf(max_val), 0.0, max_val)
        sum_exp = np.sum(np.exp(x_arr - max_val_clipped), axis=axis, keepdims=keepdims)
        out = max_val_clipped if keepdims else np.squeeze(max_val_clipped, axis=axis)
        return out + np.log(sum_exp)

    @staticmethod
    def stable_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
        x_arr = np.asarray(x, dtype=float)
        shifted = x_arr - np.max(x_arr, axis=axis, keepdims=True)
        exp_x = np.exp(shifted)
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

    @staticmethod
    def cross_entropy_loss(
        logits: np.ndarray, targets: np.ndarray
    ) -> tuple[float, np.ndarray]:
        logits = np.asarray(logits, dtype=float)
        targets = np.asarray(targets, dtype=float)
        n_samples = logits.shape[0]

        probs = TensorCalculusEngine.stable_softmax(logits, axis=-1)
        # Cross entropy loss: -sum(targets * log(probs + 1e-15)) / N
        loss = -float(np.sum(targets * np.log(probs + 1e-15)) / n_samples)
        # Analytical gradient of CrossEntropy + Softmax is (P - Y) / N
        grad = (probs - targets) / n_samples
        return loss, grad

    @staticmethod
    def two_layer_mlp_backward(
        x: np.ndarray,
        y: np.ndarray,
        W1: np.ndarray,
        b1: np.ndarray,
        W2: np.ndarray,
        b2: np.ndarray,
    ) -> dict[str, np.ndarray]:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        n_samples = x.shape[0]

        # Forward pass
        z1 = x @ W1 + b1
        a1 = np.maximum(0.0, z1)  # ReLU
        z2 = a1 @ W2 + b2
        loss, dlogits = TensorCalculusEngine.cross_entropy_loss(z2, y)

        # Backward pass
        # dW2 = a1^T @ dlogits
        dW2 = a1.T @ (dlogits * n_samples) / n_samples
        db2 = np.sum(dlogits * n_samples, axis=0) / n_samples

        # Gradient into hidden layer
        da1 = (dlogits * n_samples) @ W2.T
        dz1 = da1 * (z1 > 0.0)  # ReLU backward

        dW1 = x.T @ dz1 / n_samples
        db1 = np.sum(dz1, axis=0) / n_samples

        return {
            "loss": loss,
            "dW1": dW1,
            "db1": db1,
            "dW2": dW2,
            "db2": db2,
        }
