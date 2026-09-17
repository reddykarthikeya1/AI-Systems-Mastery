"""Tests for Chinchilla Optimal Compute."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_chinchilla_optimal_compute import chinchilla_optimal_compute
except ImportError:
    from p01_chinchilla_optimal_compute import chinchilla_optimal_compute


def test_chinchilla_optimal_compute():
    n, d = chinchilla_optimal_compute(6.0 * 1e18)
    assert abs(n - 1e9) < 1.0  # 1 Billion params optimal for 6e18 FLOPs
    assert abs(d - 1e9) < 1.0
