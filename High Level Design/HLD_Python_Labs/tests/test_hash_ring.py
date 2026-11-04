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


def test_deterministic_hashing_across_instances():
    """Verify that different ring instances with the same nodes produce identical routing."""
    ring1 = ConsistentHashRing(nodes=["node-A", "node-B", "node-C"], vnodes=50, hash_algo="sha256")
    ring2 = ConsistentHashRing(nodes=["node-A", "node-B", "node-C"], vnodes=50, hash_algo="sha256")

    # Tokens and mapping must be identical
    assert ring1.ring_tokens == ring2.ring_tokens
    for i in range(100):
        key = f"customer_{i}"
        assert ring1.get_node(key) == ring2.get_node(key)


def test_idempotent_node_addition():
    """Verify adding the same physical node multiple times does not corrupt the ring."""
    ring = ConsistentHashRing(nodes=["node-1"], vnodes=50)
    initial_tokens_count = len(ring.ring_tokens)
    assert initial_tokens_count == 50

    # Add duplicate node
    ring.add_node("node-1")
    ring.add_node("node-1")
    assert len(ring.ring_tokens) == 50
    assert len(ring.physical_nodes) == 1


def test_preference_list_distinct_nodes():
    ring = ConsistentHashRing(nodes=["node-A", "node-B", "node-C", "node-D"], vnodes=100)
    pref = ring.get_preference_list("order:999", n=3)

    assert len(pref) == 3
    # All nodes in preference list must be distinct physical nodes
    assert len(set(pref)) == 3


def test_preference_list_exceeding_node_count():
    """When requested replicas N exceeds total physical nodes, return all available distinct nodes."""
    ring = ConsistentHashRing(nodes=["node-A", "node-B"], vnodes=50)
    pref = ring.get_preference_list("order:123", n=5)

    assert len(pref) == 2
    assert set(pref) == {"node-A", "node-B"}


def test_node_removal_and_cleanup():
    ring = ConsistentHashRing(nodes=["s1", "s2", "s3"], vnodes=50)
    assert "s2" in ring.physical_nodes
    assert len(ring.ring_tokens) == 150

    ring.remove_node("s2")
    assert "s2" not in ring.physical_nodes
    assert len(ring.ring_tokens) == 100
    assert "s2" not in ring.token_to_node.values()

    # Keys formerly on s2 must now route to s1 or s3
    for i in range(50):
        node = ring.get_node(f"key_{i}")
        assert node in ["s1", "s3"]


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


def test_bounded_load_invalid_parameters():
    with pytest.raises(ValueError):
        BoundedLoadHashRing(load_factor=0.8)  # load_factor must be >= 1.0
