"""Tests for Bplus Tree Node Split."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_bplus_tree_node_split import bplus_tree_node_split
except ImportError:
    from p01_bplus_tree_node_split import bplus_tree_node_split


def test_bplus_tree_node_split():
    left, promo, right = bplus_tree_node_split([10, 20, 30, 40], 25, max_capacity=4)
    assert left == [10, 20]
    assert promo == 25
    assert right == [25, 30, 40]
    k, p, r = bplus_tree_node_split([10, 20], 15, max_capacity=4)
    assert k == [10, 15, 20]
    assert p is None
