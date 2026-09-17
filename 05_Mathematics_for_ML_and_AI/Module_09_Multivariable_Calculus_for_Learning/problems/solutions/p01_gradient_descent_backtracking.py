"""Reference Solution — Problem 01: Gradient Descent Backtracking

Topic: 09 Multivariable Calculus for Learning
"""

from __future__ import annotations


def gradient_descent_backtracking(curr_x: float, grad: float, loss_fn, lr: float = 1.0) -> float:
    init_loss = loss_fn(curr_x)
    step = lr
    for _ in range(5):
        cand = curr_x - step * grad
        if loss_fn(cand) <= init_loss:
            return round(cand, 4)
        step *= 0.5
    return round(curr_x - step * grad, 4)
