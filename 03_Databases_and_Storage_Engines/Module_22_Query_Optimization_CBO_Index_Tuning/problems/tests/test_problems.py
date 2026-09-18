"""Tests for Cost Based Join Order."""
from __future__ import annotations

import pytest
from p01_cost_based_join_order import cost_based_join_order


def test_cost_based_join_order():
    sizes = {'orders': 1000, 'users': 100, 'items': 50}
    selectivity = {('orders', 'users'): 0.001, ('orders', 'items'): 0.01}
    order, cost = cost_based_join_order(sizes, selectivity)
    assert len(order) == 3
    assert cost >= 0.0
