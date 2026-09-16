"""Unit tests for RL Bellman solver and REINFORCE agent."""
from __future__ import annotations

import numpy as np
import pytest
from rl_policy_gradient import BellmanValueIteration, REINFORCEAgent


def test_bellman_value_iteration_chain():
    # 2 states (0, 1), 1 action, terminal state 1 gives reward 10
    n_states = 2
    n_actions = 1
    # P[s, a, s']
    t_probs = np.zeros((n_states, n_actions, n_states))
    t_probs[0, 0, 1] = 1.0  # State 0 transitions to 1
    t_probs[1, 0, 1] = 1.0  # State 1 stays in 1

    rewards = np.array([[0.0], [10.0]])
    gamma = 0.9

    v_star = BellmanValueIteration.value_iteration(t_probs, rewards, gamma=gamma)
    # State 1 value: V(1) = 10 + 0.9 * V(1) => 0.1 * V(1) = 10 => V(1) = 100
    assert v_star[1] == pytest.approx(100.0, rel=1e-3)
    # State 0 value: V(0) = 0 + 0.9 * 100 = 90
    assert v_star[0] == pytest.approx(90.0, rel=1e-3)


def test_discounted_returns_computation():
    rewards = [1.0, 1.0, 2.0]
    gamma = 0.5
    # G_2 = 2.0
    # G_1 = 1.0 + 0.5 * 2.0 = 2.0
    # G_0 = 1.0 + 0.5 * 2.0 = 2.0
    g = REINFORCEAgent.compute_discounted_returns(rewards, gamma=gamma)
    assert np.allclose(g, np.array([2.0, 2.0, 2.0]))


def test_reinforce_policy_gradient_update():
    # 2 actions, 2 state dimensions
    weights = np.zeros((2, 2))
    state = np.array([1.0, 0.0])
    action = 0
    return_g = 5.0

    # Initial probabilities are [0.5, 0.5]
    new_weights = REINFORCEAgent.policy_gradient_step(weights, state, action, return_g, lr=0.1)

    # Action 0 probability should increase
    logits = new_weights @ state
    probs = np.exp(logits) / np.sum(np.exp(logits))
    assert probs[0] > 0.5
