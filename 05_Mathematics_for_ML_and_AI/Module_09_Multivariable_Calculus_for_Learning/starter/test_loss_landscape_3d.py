"""Unit tests for 3D Loss Landscape & Hessian Analyzer."""
from __future__ import annotations

import numpy as np
import pytest
from loss_landscape_3d import (
    classify_critical_point,
    rosenbrock,
    rosenbrock_grad,
    rosenbrock_hessian,
    simulate_gradient_descent_trajectory,
)


def test_rosenbrock_minimum() -> None:
    # Global minimum is at (1.0, 1.0) with value 0.0
    val = rosenbrock(1.0, 1.0)
    assert pytest.approx(val, abs=1e-7) == 0.0

    # Gradient at minimum must be zero
    grad = rosenbrock_grad(1.0, 1.0)
    np.testing.assert_allclose(grad, np.zeros(2), atol=1e-7)


def test_hessian_classification() -> None:
    # At minimum (1, 1), Hessian eigenvalues must be strictly positive
    h_min = rosenbrock_hessian(1.0, 1.0)
    assert classify_critical_point(h_min) == "minimum"

    # Saddle point: f(x, y) = x^2 - y^2 -> Hessian = diag(2, -2)
    h_saddle = np.array([[2.0, 0.0], [0.0, -2.0]])
    assert classify_critical_point(h_saddle) == "saddle"


def test_gradient_descent_trajectory_optimization() -> None:
    traj = simulate_gradient_descent_trajectory(
        start_pos=(-0.5, 0.5), lr=0.0005, momentum=0.8, steps=30
    )
    assert len(traj) == 31
    initial_loss = traj[0][2]
    final_loss = traj[-1][2]
    # Trajectory must make progress minimizing loss
    assert final_loss < initial_loss
