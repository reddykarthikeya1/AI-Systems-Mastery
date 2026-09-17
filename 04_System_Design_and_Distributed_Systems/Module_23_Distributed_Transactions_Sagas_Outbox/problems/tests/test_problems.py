"""Pytest suite for Distributed Transactions Sagas Outbox problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if Path.cwd().resolve() == PROB_DIR.resolve():
    if str(PROB_DIR) not in sys.path:
        sys.path.insert(0, str(PROB_DIR))
else:
    if str(SOL_DIR) not in sys.path:
        sys.path.insert(0, str(SOL_DIR))

from p01_reconcile_vector_clocks import reconcile_vector_clocks


def test_reconcile_vector_clocks():
    assert reconcile_vector_clocks({"node1": 1}, {"node1": 2}) == "B_HAPPENED_BEFORE_A"
    assert reconcile_vector_clocks({"node1": 2}, {"node1": 1}) == "A_HAPPENED_BEFORE_B"
    assert reconcile_vector_clocks({"node1": 2, "node2": 1}, {"node1": 1, "node2": 2}) == "CONCURRENT"
    assert reconcile_vector_clocks({"node1": 1}, {"node1": 1}) == "IDENTICAL"

