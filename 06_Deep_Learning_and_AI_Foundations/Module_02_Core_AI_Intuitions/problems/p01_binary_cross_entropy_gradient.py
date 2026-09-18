"""Problem 01 — Binary Cross Entropy Gradient

Topic: 02 Core AI Intuitions
Target: Production-grade implementation

Compute binary cross-entropy loss and its gradient with respect to predicted probability.

Example:
    >>> binary_cross_entropy_gradient(1.0, 0.9)
    (0.1054, -1.1111)

Hints:
    Hint 1: The gradient's sign tells you which direction nudges the
        prediction closer to the true label — for y=1 it should be negative
        (push p up), and for y=0 it should be positive (push p down).
    Hint 2: Compute `loss = -(y*log(p) + (1-y)*log(1-p))` and
        `grad = (p - y) / (p * (1 - p))` directly from the clamped
        probability.
    Hint 3: Clamp `p` into `[eps, 1 - eps]` with `min(max(...))` before
        using it anywhere, rather than only adding eps inside the log —
        clamping is what actually keeps both `log(p)`/`log(1-p)` and the
        gradient's denominator away from zero when `y_pred` is exactly 0.0
        or 1.0. Round both outputs to 4 decimal places.
"""

from __future__ import annotations


def binary_cross_entropy_gradient(y_true: float, y_pred: float, eps: float = 1e-7) -> tuple[float, float]:
    """BCE = - (y * log(p + eps) + (1 - y) * log(1 - p + eps))
    grad = (p - y) / ((p + eps) * (1 - p + eps))
    Returns (loss, grad) rounded to 4 decimals.
    """
    raise NotImplementedError("Implement binary_cross_entropy_gradient")
