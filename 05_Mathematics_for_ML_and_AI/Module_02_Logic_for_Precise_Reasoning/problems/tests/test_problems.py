"""Tests for Boolean Satisfiability Dpll."""
from __future__ import annotations

import pytest
from p01_boolean_satisfiability_dpll import boolean_satisfiability_dpll


def test_boolean_satisfiability_dpll():
    clauses = [[1, -2], [2, 3]]
    assert boolean_satisfiability_dpll(clauses, {1: True, 2: False, 3: True}) is True
    assert boolean_satisfiability_dpll(clauses, {1: False, 2: True, 3: False}) is False
