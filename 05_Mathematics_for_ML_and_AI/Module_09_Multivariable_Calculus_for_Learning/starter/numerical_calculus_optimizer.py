"""Starter template for numerical calculus and optimizer."""
from __future__ import annotations

from collections.abc import Callable

import numpy as np


class NumericalCalculus:
    """Numerical gradients, Jacobians, Softmax calculus, and gradient descent."""

    @staticmethod
    def numerical_gradient(
        func: Callable[[np.ndarray], float], x: np.ndarray, eps: float = 1e-5
    ) -> np.ndarray:
        """Compute gradient using two-sided central difference: (f(x+eps) - f(x-eps)) / (2*eps)."""
        raise NotImplementedError

    @staticmethod
    def numerical_jacobian(
        func: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-5
    ) -> np.ndarray:
        """Compute Jacobian matrix for vector-valued function using central difference."""
        raise NotImplementedError

    @staticmethod
    def softmax(z: np.ndarray) -> np.ndarray:
        """Compute numerically stable Softmax probabilities."""
        raise NotImplementedError

    @staticmethod
    def softmax_jacobian(z: np.ndarray) -> np.ndarray:
        """Compute exact analytical Jacobian matrix of Softmax: diag(s) - s @ s.T."""
        raise NotImplementedError

    @staticmethod
    def gradient_descent_with_momentum(
        grad_fn: Callable[[np.ndarray], np.ndarray],
        x0: np.ndarray,
        lr: float = 0.05,
        momentum: float = 0.9,
        steps: int = 50,
    ) -> np.ndarray:
        """Run gradient descent with momentum to find the minimum."""
        raise NotImplementedError
