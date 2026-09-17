"""Unit tests for NumericalCalculus."""
from __future__ import annotations

import numpy as np
from numerical_calculus_optimizer import NumericalCalculus


def test_numerical_gradient_quadratic():
    # f(x, y) = 3*x^2 + 2*y^2 + 4*x - 6*y + 10
    # grad_x = 6*x + 4, grad_y = 4*y - 6
    def func(v: np.ndarray) -> float:
        return float(3.0 * v[0] ** 2 + 2.0 * v[1] ** 2 + 4.0 * v[0] - 6.0 * v[1] + 10.0)

    point = np.array([2.0, 3.0])
    num_grad = NumericalCalculus.numerical_gradient(func, point)
    exact_grad = np.array([6.0 * 2.0 + 4.0, 4.0 * 3.0 - 6.0])

    assert np.allclose(num_grad, exact_grad, atol=1e-5)


def test_softmax_jacobian_matches_numerical():
    z = np.array([1.5, 0.2, -0.8])
    analytical_jac = NumericalCalculus.softmax_jacobian(z)
    numerical_jac = NumericalCalculus.numerical_jacobian(NumericalCalculus.softmax, z)

    assert np.allclose(analytical_jac, numerical_jac, atol=1e-5)


def test_gradient_descent_convergence():
    # Minimize f(x) = (x[0] - 3)^2 + (x[1] + 2)^2
    # Minimum is at [3.0, -2.0]
    def grad_fn(x: np.ndarray) -> np.ndarray:
        return np.array([2.0 * (x[0] - 3.0), 2.0 * (x[1] + 2.0)])

    x_start = np.array([0.0, 0.0])
    x_opt = NumericalCalculus.gradient_descent_with_momentum(
        grad_fn, x_start, lr=0.1, momentum=0.8, steps=100
    )
    assert np.allclose(x_opt, np.array([3.0, -2.0]), atol=1e-3)
