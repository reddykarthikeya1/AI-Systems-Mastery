"""Tests for Query Expansion Hypothetical."""
from __future__ import annotations

import pytest
from p01_query_expansion_hypothetical import query_expansion_hypothetical


def test_query_expansion_hypothetical():
    res = query_expansion_hypothetical("What is Raft?", "Raft is a consensus algorithm for distributed state machines.")
    assert res.startswith("Query: What is Raft? | Context: Raft is")
