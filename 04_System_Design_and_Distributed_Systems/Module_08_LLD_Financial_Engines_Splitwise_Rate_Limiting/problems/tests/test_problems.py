"""Tests for Debt Simplification Graph."""
from __future__ import annotations

import pytest
from p01_debt_simplification_graph import debt_simplification_graph


def test_debt_simplification_graph():
    balances = {'Alice': 50.0, 'Bob': -30.0, 'Charlie': -20.0}
    txs = debt_simplification_graph(balances)
    assert len(txs) == 2
    assert sum(amt for _, _, amt in txs) == 50.0
