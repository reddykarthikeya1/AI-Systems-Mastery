"""Tests for Orthogonal Projection Subspace."""
from __future__ import annotations

import pytest
from p01_orthogonal_projection_subspace import orthogonal_projection_subspace


def test_orthogonal_projection_subspace():
    # Basis along x-axis
    proj = orthogonal_projection_subspace([3.0, 4.0], [[1.0, 0.0]])
    assert proj == [3.0, 0.0]
