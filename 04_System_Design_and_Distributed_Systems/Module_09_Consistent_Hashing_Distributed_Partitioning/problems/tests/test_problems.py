"""Tests for Consistent Hash Ring Vnodes."""
from __future__ import annotations

import pytest
from p01_consistent_hash_ring_vnodes import consistent_hash_ring_vnodes


def test_consistent_hash_ring_vnodes():
    nodes = ['server_a', 'server_b', 'server_c']
    node = consistent_hash_ring_vnodes(nodes, 5, 'user:12345')
    assert node in nodes
    # Deterministic mapping
    assert consistent_hash_ring_vnodes(nodes, 5, 'user:12345') == node
