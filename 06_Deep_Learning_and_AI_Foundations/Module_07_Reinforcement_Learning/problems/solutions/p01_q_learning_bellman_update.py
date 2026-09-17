"""Reference Solution — Problem 01: Q Learning Bellman Update

Topic: 07 Reinforcement Learning
"""

from __future__ import annotations


def q_learning_bellman_update(curr_q: float, reward: float, next_q_max: float, gamma: float = 0.9, alpha: float = 0.1) -> float:
    target = reward + gamma * next_q_max
    td_error = target - curr_q
    new_q = curr_q + alpha * td_error
    return round(new_q, 4)
