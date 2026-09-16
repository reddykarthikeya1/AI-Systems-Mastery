"""Production solution for RL Bellman solver and REINFORCE agent."""
from __future__ import annotations

import numpy as np


class BellmanValueIteration:
    """Solves optimal state values for discrete Markov Decision Processes."""

    @staticmethod
    def value_iteration(
        transition_probs: np.ndarray,
        rewards: np.ndarray,
        gamma: float = 0.9,
        tol: float = 1e-6,
    ) -> np.ndarray:
        # transition_probs: shape (n_states, n_actions, n_states)
        # rewards: shape (n_states, n_actions)
        n_states, _n_actions = rewards.shape
        v = np.zeros(n_states, dtype=float)

        while True:
            # Q(s, a) = R(s, a) + gamma * sum_{s'} P(s'|s,a) * V(s')
            # Shape: (n_states, n_actions)
            q_values = rewards + gamma * np.sum(transition_probs * v[None, None, :], axis=2)
            v_next = np.max(q_values, axis=1)

            delta = np.max(np.abs(v_next - v))
            v = v_next
            if delta < tol:
                break
        return v


class REINFORCEAgent:
    """Policy gradient agent using parameter update: theta += alpha * grad(log pi) * G."""

    @staticmethod
    def compute_discounted_returns(rewards: list[float], gamma: float = 0.99) -> np.ndarray:
        t_steps = len(rewards)
        returns = np.zeros(t_steps, dtype=float)
        running_g = 0.0
        for t in reversed(range(t_steps)):
            running_g = rewards[t] + gamma * running_g
            returns[t] = running_g
        return returns

    @staticmethod
    def policy_gradient_step(
        weights: np.ndarray,
        state: np.ndarray,
        action: int,
        return_g: float,
        lr: float = 0.01,
    ) -> np.ndarray:
        # Linear Softmax Policy: logits = weights @ state
        # weights: (n_actions, state_dim)
        logits = weights @ state
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)

        # grad_logits = one_hot(action) - probs
        grad_logits = -probs
        grad_logits[action] += 1.0

        # grad_weights = grad_logits outer state
        grad_weights = np.outer(grad_logits, state)
        # Gradient ascent step: theta <- theta + lr * grad * G
        return weights + lr * grad_weights * return_g
