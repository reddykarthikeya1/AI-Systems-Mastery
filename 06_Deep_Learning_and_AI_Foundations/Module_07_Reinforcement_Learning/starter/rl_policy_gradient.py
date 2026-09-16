"""Starter template for RL Bellman solver and REINFORCE agent."""
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
        """Run Bellman value iteration until convergence:
        V(s) = max_a sum_s' P(s'|s,a)[R + gamma*V(s')].
        """
        raise NotImplementedError


class REINFORCEAgent:
    """Policy gradient agent using parameter update: theta += alpha * grad(log pi) * G."""

    @staticmethod
    def compute_discounted_returns(rewards: list[float], gamma: float = 0.99) -> np.ndarray:
        """Compute cumulative discounted returns G_t = sum_{k=0} gamma^k * r_{t+k+1}."""
        raise NotImplementedError

    @staticmethod
    def policy_gradient_step(
        weights: np.ndarray,
        state: np.ndarray,
        action: int,
        return_g: float,
        lr: float = 0.01,
    ) -> np.ndarray:
        """Update softmax linear policy weights using REINFORCE gradient."""
        raise NotImplementedError
