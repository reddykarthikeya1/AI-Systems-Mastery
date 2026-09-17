"""Tests for Ivf Flat Nearest Neighbors."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_ivf_flat_nearest_neighbors import ivf_flat_nearest_neighbors
except ImportError:
    from p01_ivf_flat_nearest_neighbors import ivf_flat_nearest_neighbors


def test_ivf_flat_nearest_neighbors():
    centroids = [[0.0, 0.0], [10.0, 10.0]]
    clusters = {
        0: [(1, [0.1, 0.1]), (2, [0.2, 0.2])],
        1: [(3, [9.9, 9.9]), (4, [10.1, 10.1])]
    }
    top = ivf_flat_nearest_neighbors([0.05, 0.05], centroids, clusters, nprobe=1)
    assert top == [1, 2]
