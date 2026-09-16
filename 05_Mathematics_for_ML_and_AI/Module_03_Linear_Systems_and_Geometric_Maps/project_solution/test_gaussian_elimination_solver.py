"""Unit tests for GaussianEliminationSolver."""
from __future__ import annotations

import numpy as np
import pytest
from gaussian_elimination_solver import GaussianEliminationSolver


def test_solve_simple_system():
    # 2x + y = 5
    # x + 3y = 5
    # Solution: x = 2, y = 1
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    b = np.array([5.0, 5.0])
    x = GaussianEliminationSolver.solve(A, b)
    assert np.allclose(x, [2.0, 1.0])
    assert np.allclose(A @ x, b)


def test_singular_matrix_raises_value_error():
    # Singular: Row 2 is 2x Row 1
    A = np.array([[1.0, 2.0], [2.0, 4.0]])
    b = np.array([3.0, 6.0])
    with pytest.raises(ValueError, match="singular"):
        GaussianEliminationSolver.solve(A, b)


def test_determinant():
    A = np.array([[3.0, 2.0], [1.0, 4.0]])
    # det = 3*4 - 2*1 = 10
    det = GaussianEliminationSolver.determinant(A)
    assert pytest.approx(det) == 10.0

    singular = np.array([[1.0, 2.0], [2.0, 4.0]])
    assert pytest.approx(GaussianEliminationSolver.determinant(singular)) == 0.0
