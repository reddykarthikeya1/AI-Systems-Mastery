"""Unit tests for BasisRankNullspace."""
from __future__ import annotations

import numpy as np
from basis_rank_nullspace import BasisRankNullspace


def test_matrix_rank():
    # Full rank 2x2
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert BasisRankNullspace.matrix_rank(A) == 2

    # Rank 1: second row is 2x first row
    B = np.array([[1.0, 2.0], [2.0, 4.0]])
    assert BasisRankNullspace.matrix_rank(B) == 1


def test_linear_independence():
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    v3 = np.array([1.0, 1.0, 0.0])  # Dependent on v1 and v2

    assert BasisRankNullspace.is_linearly_independent([v1, v2])
    assert not BasisRankNullspace.is_linearly_independent([v1, v2, v3])


def test_nullspace_property():
    # A has rank 1, nullspace has dimension 2 - 1 = 1
    A = np.array([[1.0, 2.0], [2.0, 4.0]])
    null_basis = BasisRankNullspace.nullspace_basis(A)
    assert null_basis.shape[1] == 1  # 1 null vector
    # A @ null_vector must equal 0
    assert np.allclose(A @ null_basis, 0.0)
