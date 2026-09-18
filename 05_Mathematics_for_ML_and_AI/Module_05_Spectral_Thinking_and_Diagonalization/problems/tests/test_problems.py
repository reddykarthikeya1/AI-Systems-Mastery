"""Tests for Power Iteration Eigenvalue."""
from __future__ import annotations

import pytest
from p01_power_iteration_eigenvalue import power_iteration_eigenvalue


def test_power_iteration_eigenvalue():
    A = [[2.0, 1.0], [1.0, 2.0]]
    val, vec = power_iteration_eigenvalue(A, 20)
    assert abs(val - 3.0) < 0.05
