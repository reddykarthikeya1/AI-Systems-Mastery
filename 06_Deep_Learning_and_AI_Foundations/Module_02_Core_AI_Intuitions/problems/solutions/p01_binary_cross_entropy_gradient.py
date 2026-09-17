"""Reference Solution — Problem 01: Binary Cross Entropy Gradient

Topic: 02 Core AI Intuitions
"""

from __future__ import annotations


def binary_cross_entropy_gradient(y_true: float, y_pred: float, eps: float = 1e-7) -> tuple[float, float]:
    import math
    p = min(max(y_pred, eps), 1.0 - eps)
    loss = - (y_true * math.log(p) + (1.0 - y_true) * math.log(1.0 - p))
    grad = (p - y_true) / (p * (1.0 - p))
    return (round(loss, 4), round(grad, 4))
