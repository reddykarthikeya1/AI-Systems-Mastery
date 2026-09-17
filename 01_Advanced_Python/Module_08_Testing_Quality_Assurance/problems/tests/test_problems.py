"""Tests for Property-Based Matrix Invariant."""
from __future__ import annotations

import pytest
from p01_property_matrix_check import verify_matrix_symmetry


def test_verify_matrix_symmetry():
    assert verify_matrix_symmetry([[1, 2], [2, 1]]) is True
    assert verify_matrix_symmetry([[1, 2], [3, 1]]) is False
    assert verify_matrix_symmetry([]) is True
