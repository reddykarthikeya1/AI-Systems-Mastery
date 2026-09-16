"""Production reference implementation for 3D Loss Landscape & Hessian Analyzer."""
from __future__ import annotations

import numpy as np


def rosenbrock(x: float, y: float, a: float = 1.0, b: float = 100.0) -> float:
    """Evaluate Rosenbrock banana function: (a - x)^2 + b * (y - x^2)^2."""
    return float((a - x) ** 2 + b * (y - x ** 2) ** 2)


def rosenbrock_grad(x: float, y: float, a: float = 1.0, b: float = 100.0) -> np.ndarray:
    """Compute analytical gradient [df/dx, df/dy] of Rosenbrock function.

    df/dx = -2 * (a - x) - 4 * b * x * (y - x^2)
    df/dy = 2 * b * (y - x^2)
    """
    df_dx = -2.0 * (a - x) - 4.0 * b * x * (y - x ** 2)
    df_dy = 2.0 * b * (y - x ** 2)
    return np.array([df_dx, df_dy], dtype=np.float64)


def rosenbrock_hessian(x: float, y: float, b: float = 100.0) -> np.ndarray:
    """Compute 2x2 analytical Hessian matrix of Rosenbrock function.

    d2f/dx2 = 2 - 4 * b * y + 12 * b * x^2
    d2f/dxdy = -4 * b * x
    d2f/dydx = -4 * b * x
    d2f/dy2 = 2 * b
    """
    h_xx = 2.0 - 4.0 * b * y + 12.0 * b * (x ** 2)
    h_xy = -4.0 * b * x
    h_yy = 2.0 * b
    return np.array([[h_xx, h_xy], [h_xy, h_yy]], dtype=np.float64)


def classify_critical_point(hessian: np.ndarray) -> str:
    """Classify critical point using Hessian eigenvalues.

    - If all eigenvalues > 0: local minimum
    - If all eigenvalues < 0: local maximum
    - If mixed signs: saddle point
    """
    eigenvalues = np.linalg.eigvals(hessian)
    if np.all(eigenvalues > 1e-7):
        return "minimum"
    if np.all(eigenvalues < -1e-7):
        return "maximum"
    return "saddle"


def simulate_gradient_descent_trajectory(
    start_pos: tuple[float, float],
    lr: float = 0.001,
    momentum: float = 0.9,
    steps: int = 50,
) -> list[tuple[float, float, float]]:
    """Simulate gradient descent with momentum on Rosenbrock surface.

    Returns list of (x, y, loss) tuples along the trajectory.
    """
    x, y = start_pos
    vx, vy = 0.0, 0.0
    trajectory = [(x, y, rosenbrock(x, y))]

    for _ in range(steps):
        grad = rosenbrock_grad(x, y)
        vx = momentum * vx + lr * grad[0]
        vy = momentum * vy + lr * grad[1]
        x -= vx
        y -= vy
        trajectory.append((x, y, rosenbrock(x, y)))

    return trajectory
