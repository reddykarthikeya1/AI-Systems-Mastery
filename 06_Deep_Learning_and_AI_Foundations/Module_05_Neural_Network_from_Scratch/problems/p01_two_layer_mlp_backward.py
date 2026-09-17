"""Problem 01 — Two Layer Mlp Backward

Topic: 05 Neural Network from Scratch
Target: Production-grade implementation

Compute forward activations and gradient of weights for a 2-layer MLP with ReLU.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def two_layer_mlp_backward(x: float, y: float, w1: float, w2: float) -> tuple[float, float]:
    """Forward:
    h = max(0.0, w1 * x)
    y_hat = w2 * h
    loss = 0.5 * (y_hat - y) ** 2
    Backward:
    Compute (grad_w1, grad_w2).
    Returns (grad_w1, grad_w2) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement two_layer_mlp_backward")
