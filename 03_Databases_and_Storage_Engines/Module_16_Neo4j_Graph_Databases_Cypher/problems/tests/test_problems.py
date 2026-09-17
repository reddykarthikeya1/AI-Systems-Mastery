"""Tests for Bidirectional Graph Expansion."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_bidirectional_graph_expansion import bidirectional_graph_expansion
except ImportError:
    from p01_bidirectional_graph_expansion import bidirectional_graph_expansion


def test_bidirectional_graph_expansion():
    adj = {
        'A': ['B'], 'B': ['A', 'C'], 'C': ['B', 'D'], 'D': ['C', 'E'], 'E': ['D']
    }
    assert bidirectional_graph_expansion(adj, 'A', 'E', 5) == 4
    assert bidirectional_graph_expansion(adj, 'A', 'E', 2) == -1
    assert bidirectional_graph_expansion(adj, 'A', 'A', 5) == 0
