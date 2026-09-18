"""Problem 01 — Two Layer Mlp Backward

Topic: 05 Neural Network from Scratch
Target: Production-grade implementation

Compute forward activations and gradient of weights for a 2-layer MLP with ReLU.

Example:
    >>> two_layer_mlp_backward(2.0, 4.0, 1.0, 1.0)
    (-4.0, -4.0)

Hints:
    Hint 1: This is a single chain-rule walk backward through the same
        three forward steps (z1 = w1*x, h = relu(z1), y_hat = w2*h, loss),
        each local derivative multiplying into the next.
    Hint 2: Start from `dloss/dy_hat = y_hat - y`; then `grad_w2 = dloss/dy_hat
        * h` (since y_hat = w2*h), and propagate `dloss/dh = dloss/dy_hat *
        w2` back through the ReLU and the `z1 = w1*x` product to get
        `grad_w1`.
    Hint 3: ReLU's local derivative is a hard gate, not a smooth function:
        it's 1.0 when the pre-activation z1 is strictly positive and 0.0
        otherwise (including exactly at z1 == 0) — multiply that gate into
        the backward chain for grad_w1 before rounding both gradients to
        4 decimal places.
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
