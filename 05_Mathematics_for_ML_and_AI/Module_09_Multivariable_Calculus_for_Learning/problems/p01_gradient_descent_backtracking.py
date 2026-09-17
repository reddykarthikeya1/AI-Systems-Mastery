"""Problem 01 — Gradient Descent Backtracking

Topic: 09 Multivariable Calculus for Learning
Target: Production-grade implementation

One step of gradient descent with Armijo condition step halving.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def gradient_descent_backtracking(curr_x: float, grad: float, loss_fn, lr: float = 1.0) -> float:
    """Step x_new = curr_x - lr * grad.
    If loss_fn(x_new) > loss_fn(curr_x): halve lr up to 5 times.
    Returns best x_new rounded to 4 decimals.
    """
    raise NotImplementedError("Implement gradient_descent_backtracking")
