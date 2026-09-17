"""Tests for Q Learning Bellman Update."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_q_learning_bellman_update import q_learning_bellman_update
except ImportError:
    from p01_q_learning_bellman_update import q_learning_bellman_update


def test_q_learning_bellman_update():
    # curr_q = 0, reward = 10, next_q_max = 5. target = 10 + 4.5 = 14.5. delta = 1.45.
    assert q_learning_bellman_update(0.0, 10.0, 5.0, 0.9, 0.1) == 1.45
