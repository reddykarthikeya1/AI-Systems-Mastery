"""Automated pytest test suite for Module 07 Oracle SGA & Storage Engine."""

import pytest
from oracle_sga_engine import (
    DatabaseBufferCache,
    LibraryCache,
    RedoLogBuffer,
    TablespaceStorage,
)


def test_library_cache_hard_vs_soft_parse() -> None:
    cache = LibraryCache()

    # Query 1: Hard parse
    plan1, was_soft1 = cache.parse_and_get_plan("SELECT * FROM EMPLOYEES WHERE DEPT = 10")
    assert was_soft1 is False
    assert cache.hard_parses == 1
    assert cache.soft_parses == 0

    # Query 2: Identical query -> Soft parse
    plan2, was_soft2 = cache.parse_and_get_plan("SELECT * FROM EMPLOYEES WHERE DEPT = 10")
    assert was_soft2 is True
    assert plan1 == plan2
    assert cache.soft_parses == 1


def test_bind_variable_cursor_sharing() -> None:
    cache = LibraryCache()
    normalized = "SELECT * FROM ORDERS WHERE ORDER_ID = :1"

    # User A passes order 101 with bind variable
    p1, s1 = cache.parse_and_get_plan("SELECT * FROM ORDERS WHERE ORDER_ID = 101", bind_normalized_sql=normalized)
    assert s1 is False

    # User B passes order 999 with bind variable -> Shares cursor!
    p2, s2 = cache.parse_and_get_plan("SELECT * FROM ORDERS WHERE ORDER_ID = 999", bind_normalized_sql=normalized)
    assert s2 is True
    assert p1 == p2


def test_buffer_cache_touch_count_aging() -> None:
    cache = DatabaseBufferCache(capacity_blocks=3)

    # Load block 1 and touch 5 times
    for _ in range(5):
        cache.access_block(1, {"val": "popular_data"})

    # Load block 2 and touch 2 times
    for _ in range(2):
        cache.access_block(2, {"val": "moderate_data"})

    # Load block 3 and touch 1 time
    cache.access_block(3, {"val": "cold_data"})

    # Capacity of 3 is reached. Now access block 4.
    # Block 3 has touch_count=1, so it must be evicted first!
    cache.access_block(4, {"val": "new_data"})

    assert 1 in cache._cache  # Retained (touch_count=5)
    assert 2 in cache._cache  # Retained (touch_count=2)
    assert 3 not in cache._cache  # Evicted!
    assert 4 in cache._cache  # Newly admitted


def test_buffer_cache_dirty_blocks() -> None:
    cache = DatabaseBufferCache(capacity_blocks=3)
    cache.access_block(10)
    cache.access_block(20)

    assert len(cache.get_dirty_blocks()) == 0

    # Modify block 10
    cache.mark_dirty(10)
    dirty = cache.get_dirty_blocks()
    assert len(dirty) == 1
    assert dirty[0].block_id == 10


def test_redo_log_buffer_flush_on_commit() -> None:
    redo = RedoLogBuffer(buffer_size=10)
    redo.append_redo_record("CHANGE #1: INSERT INTO USERS (ID, NAME) VALUES (1, 'ALICE')")
    redo.append_redo_record("CHANGE #2: UPDATE ACCOUNTS SET BAL = 500 WHERE ID = 1")

    assert len(redo._buffer) == 2
    assert len(redo.flushed_to_online_redo_log) == 0

    # LGWR commit flush
    flushed = redo.commit()
    assert flushed == 2
    assert len(redo._buffer) == 0
    assert len(redo.flushed_to_online_redo_log) == 2


def test_tablespace_extent_allocation_and_hwm() -> None:
    ts = TablespaceStorage("USERS_TS", blocks_per_extent=8)
    ext1 = ts.allocate_extent()
    assert ext1.extent_id == 1
    assert ext1.start_block_id == 1
    assert ext1.block_count == 8

    # Insert into block 5
    ts.insert_row_into_block(5)
    assert ts.high_water_mark_block == 5

    # Insert into unallocated block raises error
    with pytest.raises(ValueError, match="Block #20 has not been allocated"):
        ts.insert_row_into_block(20)

    # Allocate second extent (blocks 9..16)
    ext2 = ts.allocate_extent()
    assert ext2.extent_id == 2
    assert ext2.start_block_id == 9

    # Now block 12 can be written to
    ts.insert_row_into_block(12)
    assert ts.high_water_mark_block == 12
