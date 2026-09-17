"""Unit tests for PowerIterationPageRank."""
from __future__ import annotations

import numpy as np
import pytest
from power_iteration_pagerank import PowerIterationPageRank


def test_dominant_eigenvalue():
    # Matrix with known eigenvalues 5 and 2
    A = np.array([[4.0, 2.0], [1.0, 3.0]])
    val, vec = PowerIterationPageRank.dominant_eigen(A)
    assert pytest.approx(val, rel=1e-4) == 5.0
    # A @ v = lambda * v
    assert np.allclose(A @ vec, val * vec, atol=1e-4)


def test_pagerank_equilibrium():
    # 3-page network: Page 0 and 1 link to Page 2
    adj = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
    ])
    scores = PowerIterationPageRank.compute_pagerank(adj, damping=0.85)
    assert len(scores) == 3
    assert np.sum(scores) == pytest.approx(1.0)
    # Page 2 has the most incoming links, so it must have the highest rank
    assert scores[2] > scores[0]
    assert scores[2] > scores[1]
