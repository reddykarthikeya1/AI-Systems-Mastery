"""Tests for Consistent Hash Ring and Google Bounded Loads (Chapter 07)."""
import pytest
from ch07_consistent_hashing.hash_ring import (
    ConsistentHashRing,
    BoundedLoadHashRing,
)


def test_consistent_hash_ring_lookup():
    ring = ConsistentHashRing(nodes=["node-1", "node-2", "node-3"], vnodes=100)

    # Consistent routing: Same key routes to same node
    node_a1 = ring.get_node("user_1001")
    node_a2 = ring.get_node("user_1001")
    assert node_a1 is not None
    assert node_a1 == node_a2
    assert node_a1 in ["node-1", "node-2", "node-3"]


def test_preference_list_distinct_nodes():
    ring = ConsistentHashRing(nodes=["node-A", "node-B", "node-C", "node-D"], vnodes=100)
    pref = ring.get_preference_list("order:999", n=3)

    assert len(pref) == 3
    # All nodes in preference list must be distinct physical nodes
    assert len(set(pref)) == 3


def test_redistribution_analysis():
    ring = ConsistentHashRing(nodes=["node-1", "node-2", "node-3"], vnodes=150)
    test_keys = [f"key_{i}" for i in range(1000)]

    analysis = ring.analyze_redistribution(test_keys, new_node="node-4")

    # With 3 nodes, adding 4th node ideally migrates ~ 1/4 = 0.25 of keys
    fraction = analysis["migrated_fraction"]
    ideal = analysis["theoretical_ideal"]

    assert ideal == pytest.approx(0.25, abs=0.01)
    # Statistical tolerance for 150 vnodes
    assert 0.15 <= fraction <= 0.35


def test_bounded_load_hash_ring():
    # 3 nodes with load factor 1.25
    ring = BoundedLoadHashRing(nodes=["s1", "s2", "s3"], vnodes=100, load_factor=1.25)

    # Assign 60 keys
    for i in range(60):
        assigned = ring.assign_key(f"request_{i}")
        assert assigned in ["s1", "s2", "s3"]

    assert ring.total_load == 60
    # Average load is 60 / 3 = 20. Max allowed is ceil(1.25 * 20) = 25.
    for node, load in ring.node_loads.items():
        assert load <= 25

    # Release load
    ring.release_load("s1", 5)
    assert ring.total_load == 55
