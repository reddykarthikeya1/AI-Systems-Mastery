"""Unit tests for Consistent Hash Ring with Virtual Nodes."""

from __future__ import annotations

from consistent_hash_ring import ConsistentHashRing


def test_deterministic_key_lookup() -> None:
    ring = ConsistentHashRing(nodes=["node-A", "node-B", "node-C"], vnodes=100)

    # Identical keys must always resolve to the exact same physical node
    node1 = ring.get_node("user_session_99214")
    node2 = ring.get_node("user_session_99214")
    assert node1 is not None
    assert node1 == node2
    assert node1 in {"node-A", "node-B", "node-C"}


def test_minimal_key_migration_on_node_addition() -> None:
    """Core property of consistent hashing: adding node N+1 migrates only ~1/(N+1) keys."""
    initial_nodes = ["node-1", "node-2", "node-3"]
    ring = ConsistentHashRing(nodes=initial_nodes, vnodes=150)

    keys = [f"cache_key_{i}" for i in range(1000)]
    mapping_before = {k: ring.get_node(k) for k in keys}

    # Add a 4th node
    ring.add_node("node-4")
    mapping_after = {k: ring.get_node(k) for k in keys}

    # Count how many keys changed their destination node
    migrated_keys = [k for k in keys if mapping_before[k] != mapping_after[k]]
    migration_ratio = len(migrated_keys) / len(keys)

    # In naive modulo hashing, adding 1 node moves ~75% of keys!
    # In consistent hashing, ideal migration to node-4 is 1/4 = 25%.
    # With 150 vnodes, migration should be tightly bounded between 15% and 35%.
    assert 0.15 <= migration_ratio <= 0.35

    # Any key that DID migrate must have migrated to the newly added node-4!
    for k in migrated_keys:
        assert mapping_after[k] == "node-4"


def test_minimal_key_migration_on_node_removal() -> None:
    ring = ConsistentHashRing(nodes=["node-1", "node-2", "node-3"], vnodes=150)
    keys = [f"item_{i}" for i in range(1000)]
    mapping_before = {k: ring.get_node(k) for k in keys}

    # Remove node-3
    ring.remove_node("node-3")
    mapping_after = {k: ring.get_node(k) for k in keys}

    # Keys that were on node-1 or node-2 must NOT have moved!
    for k in keys:
        if mapping_before[k] != "node-3":
            assert mapping_after[k] == mapping_before[k]
        else:
            # Keys previously on node-3 must now be reassigned to node-1 or node-2
            assert mapping_after[k] in {"node-1", "node-2"}


def test_preference_list_returns_distinct_physical_nodes() -> None:
    ring = ConsistentHashRing(nodes=["node-A", "node-B", "node-C", "node-D"], vnodes=100)

    replicas = ring.get_preference_list("order_payload_77", count=3)
    assert len(replicas) == 3
    # Replicas must be 3 unique physical nodes
    assert len(set(replicas)) == 3
    for r in replicas:
        assert r in ring.physical_nodes


def test_virtual_nodes_variance_reduction() -> None:
    # 1000 keys across 4 nodes with 200 vnodes should have standard deviation < 25% of mean
    ring = ConsistentHashRing(nodes=["srv-1", "srv-2", "srv-3", "srv-4"], vnodes=200)
    keys = [f"metric_series_{i}" for i in range(2000)]

    stats = ring.get_distribution_stats(keys)
    assert stats["std_dev_ratio"] < 0.25  # standard deviation is less than 25% of expected load
