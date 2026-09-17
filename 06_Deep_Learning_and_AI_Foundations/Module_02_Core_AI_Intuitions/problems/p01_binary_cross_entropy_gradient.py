"""Problem 01 — Binary Cross Entropy Gradient

Topic: 02 Core AI Intuitions
Target: Production-grade implementation

Compute binary cross-entropy loss and its gradient with respect to predicted probability.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def binary_cross_entropy_gradient(y_true: float, y_pred: float, eps: float = 1e-7) -> tuple[float, float]:
    """BCE = - (y * log(p + eps) + (1 - y) * log(1 - p + eps))
    grad = (p - y) / ((p + eps) * (1 - p + eps))
    Returns (loss, grad) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement binary_cross_entropy_gradient")
