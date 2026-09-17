"""Reference Solution — Problem 01: Two Layer Mlp Backward

Topic: 05 Neural Network from Scratch
"""

from __future__ import annotations


def two_layer_mlp_backward(x: float, y: float, w1: float, w2: float) -> tuple[float, float]:
    z1 = w1 * x
    h = max(0.0, z1)
    y_hat = w2 * h
    dloss_dyhat = y_hat - y
    grad_w2 = dloss_dyhat * h
    dloss_dh = dloss_dyhat * w2
    dh_dz1 = 1.0 if z1 > 0 else 0.0
    grad_w1 = dloss_dh * dh_dz1 * x
    return (round(grad_w1, 4), round(grad_w2, 4))
