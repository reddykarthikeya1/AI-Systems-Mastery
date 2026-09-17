"""Tests for Gaussian Elimination Solve."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_gaussian_elimination_solve import gaussian_elimination_solve
except ImportError:
    from p01_gaussian_elimination_solve import gaussian_elimination_solve


def test_gaussian_elimination_solve():
    A = [[2.0, 1.0], [1.0, 3.0]]
    b = [5.0, 5.0]
    # 2x + y = 5, x + 3y = 5 -> x = 2, y = 1
    x = gaussian_elimination_solve(A, b)
    assert x == [2.0, 1.0]
