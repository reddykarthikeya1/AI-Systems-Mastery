"""Module 15 Test Suite: LSM-Trees, Compaction & DynamoDB Single-Table Design."""

from __future__ import annotations

from lsm_dynamo_engine import (
    BloomFilter,
    DynamoDBSingleTableEngine,
    LSMTreeEngine,
    MemTable,
)


def test_bloom_filter_zero_false_negatives() -> None:
    bf = BloomFilter(expected_items=50, false_positive_rate=0.01)
    keys = [f"sensor:node_{i}" for i in range(50)]

    for k in keys:
        bf.add(k)

    # Mathematical property: Zero false negatives
    for k in keys:
        assert bf.contains(k) is True

    # Absent key should typically evaluate to False
    assert bf.contains("sensor:non_existent_key_99999") is False


def test_memtable_flush_to_sstable() -> None:
    memtable = MemTable(max_entries=3)
    assert not memtable.is_full()

    memtable.put("user:charlie", {"name": "Charlie"}, timestamp_us=100)
    memtable.put("user:alice", {"name": "Alice"}, timestamp_us=101)
    memtable.put("user:bob", {"name": "Bob"}, timestamp_us=102)

    assert memtable.is_full()

    sstable = memtable.flush()
    assert len(memtable.storage) == 0

    # SSTable entries must be strictly sorted by key
    sstable_keys = [entry[0] for entry in sstable.entries]
    assert sstable_keys == ["user:alice", "user:bob", "user:charlie"]

    # Point lookup via SSTable
    val, ts, is_tomb = sstable.get("user:bob")  # type: ignore[misc]
    assert val == {"name": "Bob"}
    assert ts == 102
    assert not is_tomb


def test_lsm_tree_overwrites_and_tombstones() -> None:
    # Small memtable max_entries = 2 to force flushes
    engine = LSMTreeEngine(memtable_max_entries=2)

    engine.put("k1", "v1")
    engine.put("k2", "v2")
    # Inserting 3rd item forces flush of k1 and k2 to SSTable 0
    engine.put("k3", "v3")

    assert len(engine.sstables) == 1
    assert engine.get("k1") == "v1"
    assert engine.get("k2") == "v2"
    assert engine.get("k3") == "v3"

    # Overwrite k1 in active MemTable
    engine.put("k1", "v1_updated")
    # MemTable version takes precedence over older SSTable version
    assert engine.get("k1") == "v1_updated"

    # Delete k2 (writes tombstone)
    engine.delete("k2")
    assert engine.get("k2") is None


def test_sstable_merge_compaction() -> None:
    engine = LSMTreeEngine(memtable_max_entries=2)

    # Populate multiple SSTables
    engine.put("alpha", "old_val")
    engine.put("beta", "stay_val")
    # Flush 1
    engine.put("alpha", "new_val")
    engine.delete("beta")
    # Flush 2
    engine.put("gamma", "gamma_val")
    engine.put("delta", "delta_val")

    # Force memtable contents into SSTable
    if engine.memtable.storage:
        engine.sstables.insert(0, engine.memtable.flush())

    assert len(engine.sstables) >= 2

    # Execute compaction: multi-way merge sort
    engine.compact()

    assert len(engine.sstables) == 1
    compacted = engine.sstables[0]

    # Obsolete "beta" tombstone and older "alpha" should be resolved
    compacted_keys = [entry[0] for entry in compacted.entries]
    assert "beta" not in compacted_keys  # Tombstone purged
    assert "alpha" in compacted_keys

    # Value of alpha must be the newest version
    val, _, _ = compacted.get("alpha")  # type: ignore[misc]
    assert val == "new_val"


def test_dynamodb_single_table_and_rcu_wcu() -> None:
    dynamo = DynamoDBSingleTableEngine()

    # User Profile
    wcu_profile = dynamo.put_item({
        "PK": "USER#1001",
        "SK": "PROFILE",
        "email": "user@example.com",
        "name": "Jane Doe",
    })
    assert wcu_profile >= 1.0

    # User Orders
    dynamo.put_item({"PK": "USER#1001", "SK": "ORDER#2026-001", "total": 120.0})
    dynamo.put_item({"PK": "USER#1001", "SK": "ORDER#2026-002", "total": 350.5})

    # Another tenant/user
    dynamo.put_item({"PK": "USER#2002", "SK": "PROFILE", "name": "Bob Smith"})

    # Single-table partition query: Fetch all orders for USER#1001 with 1 round-trip!
    user_orders = dynamo.query(pk="USER#1001", sk_prefix="ORDER#")
    assert len(user_orders) == 2
    assert user_orders[0]["SK"] == "ORDER#2026-001"
    assert user_orders[1]["SK"] == "ORDER#2026-002"

    # Verify RCU accounting: Strong Read vs Eventual Read
    _, strong_rcu = dynamo.get_item("USER#1001", "PROFILE", consistent_read=True)
    _, eventual_rcu = dynamo.get_item("USER#1001", "PROFILE", consistent_read=False)

    assert strong_rcu == 1.0
    assert eventual_rcu == 0.5
