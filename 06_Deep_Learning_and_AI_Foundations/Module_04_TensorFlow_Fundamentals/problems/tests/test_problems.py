"""Tests for Computational Graph Toposort."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_computational_graph_toposort import computational_graph_toposort
except ImportError:
    from p01_computational_graph_toposort import computational_graph_toposort


def test_computational_graph_toposort():
    graph = {
        'Loss': ['Pred', 'Y'],
        'Pred': ['W', 'X'],
        'W': [],
        'X': [],
        'Y': []
    }
    order = computational_graph_toposort(graph)
    assert order.index('W') < order.index('Pred')
    assert order.index('Pred') < order.index('Loss')
