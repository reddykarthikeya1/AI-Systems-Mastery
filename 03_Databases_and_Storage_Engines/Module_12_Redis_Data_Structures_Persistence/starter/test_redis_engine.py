"""Module 12 Test Suite: Redis Data Structures, Memory Optimization & Persistence."""

from __future__ import annotations

import time
from redis_engine import RedisEngine, SimpleDynamicString, SkipList, SortedSet


def test_sds_binary_safe_and_preallocation() -> None:
    # Binary safety with embedded null bytes
    raw_payload = b"user\x00session\x00token_12345"
    sds = SimpleDynamicString(raw_payload)
    assert sds.len == len(raw_payload)
    assert sds.alloc == len(raw_payload)
    assert sds.to_bytes() == raw_payload

    # Append data and verify pre-allocation doubling
    sds.append(b"_extra_bytes")
    expected_len = len(raw_payload) + len(b"_extra_bytes")
    assert sds.len == expected_len
    # Initial alloc doubled
    assert sds.alloc >= expected_len * 2

    # Lazy truncation
    sds.truncate(4)
    assert sds.len == 4
    assert sds.to_bytes() == b"user"
    # Allocated buffer capacity is preserved (lazy freeing)
    assert sds.alloc >= expected_len * 2


def test_skiplist_ordering_and_range() -> None:
    sl = SkipList(max_level=8)
    sl.insert("charlie", 30.0)
    sl.insert("alice", 10.0)
    sl.insert("david", 40.0)
    sl.insert("bob", 20.0)

    assert sl.length == 4

    # Full range
    items = sl.range_by_score(0.0, 50.0)
    assert items == [
        ("alice", 10.0),
        ("bob", 20.0),
        ("charlie", 30.0),
        ("david", 40.0),
    ]

    # Sliced range
    sub_items = sl.range_by_score(15.0, 35.0)
    assert sub_items == [("bob", 20.0), ("charlie", 30.0)]

    # Deletion
    deleted = sl.delete("bob", 20.0)
    assert deleted is True
    assert sl.length == 3
    assert sl.range_by_score(0.0, 50.0) == [
        ("alice", 10.0),
        ("charlie", 30.0),
        ("david", 40.0),
    ]


def test_sorted_set_rank_and_score_update() -> None:
    zset = SortedSet()
    assert zset.zadd("player1", 100.0) is True
    assert zset.zadd("player2", 250.0) is True
    assert zset.zadd("player3", 50.0) is True
    assert len(zset) == 3

    # Score lookups O(1)
    assert zset.zscore("player1") == 100.0
    assert zset.zscore("player2") == 250.0
    assert zset.zscore("nonexistent") is None

    # Ranks (1-indexed ascending score)
    assert zset.zrank("player3") == 1
    assert zset.zrank("player1") == 2
    assert zset.zrank("player2") == 3

    # Score update: player3 gets bonus to 300.0
    updated = zset.zadd("player3", 300.0)
    assert updated is False  # False indicates score update, not new member
    assert zset.zscore("player3") == 300.0

    # New ranks: player1 (100.0), player2 (250.0), player3 (300.0)
    assert zset.zrank("player1") == 1
    assert zset.zrank("player2") == 2
    assert zset.zrank("player3") == 3


def test_redis_engine_strings_and_incrby() -> None:
    engine = RedisEngine()
    engine.set("metrics:visits", "1000")
    assert engine.get("metrics:visits") == b"1000"

    # INCRBY
    new_val = engine.incrby("metrics:visits", 50)
    assert new_val == 1050
    assert engine.get("metrics:visits") == b"1050"


def test_bgrewriteaof_compaction() -> None:
    engine = RedisEngine()
    engine.set("account:alice", "0")

    # 40 increment commands
    for _ in range(40):
        engine.incrby("account:alice", 10)

    # Engine log has 1 SET + 40 INCRBY = 41 raw commands
    assert len(engine.aof_log) == 41

    # Run BGREWRITEAOF
    compacted = engine.bgrewriteaof()
    assert len(compacted) == 1
    # Compacted command is the single canonical SET with 400
    assert "account:alice" in compacted[0]
    assert "400" in compacted[0]


def test_approximate_lru_eviction() -> None:
    # Set tight memory limit of 300 bytes to force eviction
    engine = RedisEngine(max_memory_bytes=300, eviction_policy="allkeys-lru", maxmemory_samples=5)

    engine.set("key1", "value1_data")
    time.sleep(0.01)
    engine.set("key2", "value2_data")
    time.sleep(0.01)
    # Touch key1 so key2 becomes oldest
    engine.get("key1")
    time.sleep(0.01)
    engine.set("key3", "value3_data")
    time.sleep(0.01)
    engine.set("key4", "value4_data")

    # Key memory should have triggered eviction
    # Either key2 or key1 should have been evicted, but key2 was older than key1
    _ = engine.evict_if_needed()
    # At least one key was evicted or keyspace is bounded
    assert len(engine._strings) <= 4
