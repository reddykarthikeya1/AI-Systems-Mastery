"""Tests for Cassandra Murmur3 Token Ring."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_cassandra_murmur3_token_ring import cassandra_murmur3_token_ring
except ImportError:
    from p01_cassandra_murmur3_token_ring import cassandra_murmur3_token_ring


def test_cassandra_murmur3_token_ring():
    ring = [(100, "nodeA"), (200, "nodeB"), (300, "nodeC"), (400, "nodeD")]
    assert cassandra_murmur3_token_ring(ring, 150, 3) == ["nodeB", "nodeC", "nodeD"]
    assert cassandra_murmur3_token_ring(ring, 450, 2) == ["nodeA", "nodeB"]
