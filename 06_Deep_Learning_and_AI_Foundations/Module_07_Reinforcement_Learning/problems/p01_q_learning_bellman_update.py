"""Problem 01 — Q Learning Bellman Update

Topic: 07 Reinforcement Learning
Target: Production-grade implementation

Compute one-step Q-learning Bellman update: Q(s, a) <- Q(s, a) + alpha * (r + gamma * max_a' Q(s', a') - Q(s, a)).

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def q_learning_bellman_update(curr_q: float, reward: float, next_q_max: float, gamma: float = 0.9, alpha: float = 0.1) -> float:
    """Return new Q value rounded to 4 decimals."""
    raise NotImplementedError("Implement q_learning_bellman_update")
