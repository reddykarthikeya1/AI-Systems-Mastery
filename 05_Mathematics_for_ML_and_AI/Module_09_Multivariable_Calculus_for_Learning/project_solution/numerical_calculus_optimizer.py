"""Production solution for numerical calculus and optimizer."""
from __future__ import annotations

from collections.abc import Callable

import numpy as np


class NumericalCalculus:
    """Numerical gradients, Jacobians, Softmax calculus, and gradient descent."""

    @staticmethod
    def numerical_gradient(
        func: Callable[[np.ndarray], float], x: np.ndarray, eps: float = 1e-5
    ) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        grad = np.zeros_like(x)
        it = np.nditer(x, flags=["multi_index"], op_flags=["readwrite"])
        while not it.finished:
            idx = it.multi_index
            orig_val = x[idx]

            x[idx] = orig_val + eps
            f_plus = func(x)

            x[idx] = orig_val - eps
            f_minus = func(x)

            grad[idx] = (f_plus - f_minus) / (2.0 * eps)
            x[idx] = orig_val
            it.iternext()
        return grad

    @staticmethod
    def numerical_jacobian(
        func: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-5
    ) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        f0 = func(x)
        m = len(f0)
        n = len(x)
        jac = np.zeros((m, n), dtype=float)

        for j in range(n):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[j] += eps
            x_minus[j] -= eps
            f_plus = func(x_plus)
            f_minus = func(x_minus)
            jac[:, j] = (f_plus - f_minus) / (2.0 * eps)
        return jac

    @staticmethod
    def softmax(z: np.ndarray) -> np.ndarray:
        z = np.asarray(z, dtype=float)
        # Shift for numerical stability
        shifted_z = z - np.max(z)
        exp_z = np.exp(shifted_z)
        return exp_z / np.sum(exp_z)

    @staticmethod
    def softmax_jacobian(z: np.ndarray) -> np.ndarray:
        s = NumericalCalculus.softmax(z)
        # Analytical Jacobian: diag(s) - s s^T
        return np.diag(s) - np.outer(s, s)

    @staticmethod
    def gradient_descent_with_momentum(
        grad_fn: Callable[[np.ndarray], np.ndarray],
        x0: np.ndarray,
        lr: float = 0.05,
        momentum: float = 0.9,
        steps: int = 50,
    ) -> np.ndarray:
        x = np.asarray(x0, dtype=float).copy()
        v = np.zeros_like(x)
        for _ in range(steps):
            g = grad_fn(x)
            v = momentum * v + lr * g
            x = x - v
        return x
