"""Starter template for 3D Loss Landscape & Hessian Analyzer."""
from __future__ import annotations

import numpy as np


def rosenbrock(x: float, y: float, a: float = 1.0, b: float = 100.0) -> float:
    """Evaluate Rosenbrock banana function: (a - x)^2 + b * (y - x^2)^2."""
    raise NotImplementedError("Implement rosenbrock")


def rosenbrock_grad(x: float, y: float, a: float = 1.0, b: float = 100.0) -> np.ndarray:
    """Compute analytical gradient [df/dx, df/dy] of Rosenbrock function."""
    raise NotImplementedError("Implement rosenbrock_grad")


def rosenbrock_hessian(x: float, y: float, b: float = 100.0) -> np.ndarray:
    """Compute 2x2 analytical Hessian matrix of Rosenbrock function."""
    raise NotImplementedError("Implement rosenbrock_hessian")


def classify_critical_point(hessian: np.ndarray) -> str:
    """Classify critical point using Hessian eigenvalues: 'minimum', 'maximum', or 'saddle'."""
    raise NotImplementedError("Implement classify_critical_point")


def simulate_gradient_descent_trajectory(
    start_pos: tuple[float, float],
    lr: float = 0.001,
    momentum: float = 0.9,
    steps: int = 50,
) -> list[tuple[float, float, float]]:
    """Simulate gradient descent with momentum on Rosenbrock surface."""
    raise NotImplementedError("Implement simulate_gradient_descent_trajectory")
