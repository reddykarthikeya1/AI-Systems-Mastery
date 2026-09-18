"""Tests for Gin Inverted Index Query."""
from __future__ import annotations

import pytest
from p01_gin_inverted_index_query import gin_inverted_index_query


def test_gin_inverted_index_query():
    idx = {
        "postgres": {1, 2, 3},
        "acid": {2, 3, 4},
        "jsonb": {1, 3}
    }
    assert gin_inverted_index_query(idx, ["postgres", "acid"]) == {2, 3}
    assert gin_inverted_index_query(idx, ["postgres", "jsonb"]) == {1, 3}
    assert gin_inverted_index_query(idx, ["unknown"]) == set()
    assert gin_inverted_index_query(idx, []) == set()
