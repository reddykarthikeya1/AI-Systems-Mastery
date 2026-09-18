"""Problem 01 — Gradient Descent Backtracking

Topic: 09 Multivariable Calculus for Learning
Target: Production-grade implementation

One step of gradient descent with Armijo condition step halving.

Example:
    >>> gradient_descent_backtracking(2.0, 4.0, lambda x: x ** 2, lr=0.1)
    1.6

Hints:
    Hint 1: A gradient step is only useful if it actually makes progress —
        checking the loss at the candidate point against the loss at the
        current point tells you whether the chosen step size overshot.
    Hint 2: Compute the initial loss once, then repeatedly try
        `curr_x - step * grad`; if that candidate's loss is not greater than
        the initial loss, accept it, otherwise halve `step` and retry
        (this simplified condition, not the full Armijo slope test).
    Hint 3: Cap the halving at 5 attempts and fall back to whatever the
        smallest tried step produces rather than looping forever if the
        loss function never improves; round the returned x to 4 decimals.
"""

from __future__ import annotations


def gradient_descent_backtracking(curr_x: float, grad: float, loss_fn, lr: float = 1.0) -> float:
    """Step x_new = curr_x - lr * grad.
    If loss_fn(x_new) > loss_fn(curr_x): halve lr up to 5 times.
    Returns best x_new rounded to 4 decimals.
    """
    raise NotImplementedError("Implement gradient_descent_backtracking")
