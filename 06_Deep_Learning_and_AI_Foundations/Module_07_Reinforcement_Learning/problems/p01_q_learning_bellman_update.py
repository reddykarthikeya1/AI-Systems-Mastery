"""Problem 01 — Q Learning Bellman Update

Topic: 07 Reinforcement Learning
Target: Production-grade implementation

Compute one-step Q-learning Bellman update: Q(s, a) <- Q(s, a) + alpha * (r + gamma * max_a' Q(s', a') - Q(s, a)).

Example:
    >>> q_learning_bellman_update(0.0, 10.0, 5.0, gamma=0.9, alpha=0.1)
    1.45

Hints:
    Hint 1: The update only ever moves the current estimate a fraction of
        the way toward a "target" value built from the observed reward plus
        the discounted best future value — it never jumps straight to it.
    Hint 2: Compute the TD target `reward + gamma * next_q_max`, subtract
        `curr_q` to get the TD error, then take a step of size `alpha` in
        that error's direction: `curr_q + alpha * td_error`.
    Hint 3: `next_q_max` must already be the MAX over next-state actions —
        this function doesn't do that max itself, it only consumes the
        precomputed value — and `alpha`/`gamma` are keyword args with
        defaults, so the update still works when a caller omits them.
        Round the final Q value to 4 decimal places.
"""

from __future__ import annotations


def q_learning_bellman_update(curr_q: float, reward: float, next_q_max: float, gamma: float = 0.9, alpha: float = 0.1) -> float:
    """Return new Q value rounded to 4 decimals."""
    raise NotImplementedError("Implement q_learning_bellman_update")
