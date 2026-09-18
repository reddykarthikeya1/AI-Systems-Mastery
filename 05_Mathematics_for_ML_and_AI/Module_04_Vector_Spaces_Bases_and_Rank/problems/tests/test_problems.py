"""Tests for Gram Schmidt Orthogonalization."""
from __future__ import annotations

import pytest
from p01_gram_schmidt_orthogonalization import gram_schmidt_orthogonalization


def test_gram_schmidt_orthogonalization():
    v1 = [3.0, 1.0]
    v2 = [2.0, 2.0]
    u = gram_schmidt_orthogonalization([v1, v2])
    assert len(u) == 2
    assert abs(u[0][0] * u[1][0] + u[0][1] * u[1][1]) < 1e-3
