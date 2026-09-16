"""Module 21 Test Suite: Storage Engine Internals, Buffer Pool & B+ Tree."""

from __future__ import annotations

import pytest
from storage_engine import (
    BPlusTree,
    BufferPoolManager,
    DiskManager,
    RID,
    SlottedPage,
)


def test_slotted_page_binary_insert_and_get() -> None:
    page = SlottedPage(page_id=1, page_size=1024)
    assert page.tuple_count == 0
    assert page.free_space() == 1024 - 16

    # Insert variable-length tuples
    s0 = page.insert_tuple(b"First tuple payload")
    s1 = page.insert_tuple(b"Second much longer tuple payload data")
    s2 = page.insert_tuple(b"Short")

    assert s0 == 0
    assert s1 == 1
    assert s2 == 2
    assert page.tuple_count == 3

    # Retrieve payloads via slot index
    assert page.get_tuple(0) == b"First tuple payload"
    assert page.get_tuple(1) == b"Second much longer tuple payload data"
    assert page.get_tuple(2) == b"Short"
    assert page.get_tuple(3) is None  # Out of bounds


def test_slotted_page_free_space_exhaustion() -> None:
    # Tiny 64-byte page
    page = SlottedPage(page_id=2, page_size=64)
    # Header takes 16 bytes -> 48 bytes free
    # Insert 40 bytes (requires 4 byte slot + 40 bytes payload = 44 bytes)
    slot_ok = page.insert_tuple(b"A" * 40)
    assert slot_ok == 0

    # Remaining free space is only 4 bytes (insufficient for 4-byte slot + 1 byte payload)
    slot_fail = page.insert_tuple(b"B")
    assert slot_fail is None
    assert page.tuple_count == 1


def test_buffer_pool_manager_pinning_and_clock_eviction() -> None:
    disk = DiskManager(page_size=512)
    p0 = disk.allocate_page()
    p1 = disk.allocate_page()
    p2 = disk.allocate_page()

    # Buffer pool with only 2 memory frames
    bpm = BufferPoolManager(pool_size=2, disk_manager=disk)

    # Fetch pages 0 and 1 (both pinned with pin_count=1)
    page_0 = bpm.fetch_page(p0)
    _ = bpm.fetch_page(p1)
    page_0.insert_tuple(b"Mutated Data on Page 0")

    # Attempting to fetch p2 when all frames are pinned must raise RuntimeError
    with pytest.raises(RuntimeError):
        bpm.fetch_page(p2)

    # Unpin page 0 as dirty
    bpm.unpin_page(p0, is_dirty=True)

    # Now fetching p2 succeeds by evicting unpinned dirty page 0 (flushing it to disk)
    page_2 = bpm.fetch_page(p2)
    assert page_2.page_id == p2

    # Unpin page 1 and page 2
    bpm.unpin_page(p1, is_dirty=False)
    bpm.unpin_page(p2, is_dirty=False)

    # Fetch page 0 back from disk and verify mutated data persisted
    reloaded_p0 = bpm.fetch_page(p0)
    assert reloaded_p0.get_tuple(0) == b"Mutated Data on Page 0"


def test_bplus_tree_insertion_and_search() -> None:
    tree = BPlusTree(order=3)
    keys = [10, 20, 30, 40, 50, 60, 70]

    for k in keys:
        tree.insert(k, RID(page_id=k // 10, slot_id=k % 10))

    # Point Lookups
    for k in keys:
        rid = tree.search(k)
        assert rid is not None
        assert rid.page_id == k // 10
        assert rid.slot_id == k % 10

    # Absent key
    assert tree.search(999) is None


def test_bplus_tree_range_scan_linked_leaves() -> None:
    tree = BPlusTree(order=3)
    for k in [5, 15, 25, 35, 45, 55, 65, 75]:
        tree.insert(k, RID(page_id=1, slot_id=k))

    # Range scan [20, 60] -> 25, 35, 45, 55
    results = tree.range_scan(min_key=20, max_key=60)
    matched_keys = [k for k, _ in results]
    assert matched_keys == [25, 35, 45, 55]

    # Empty range
    assert tree.range_scan(100, 200) == []


def test_bplus_tree_fanout_vs_depth_sweep() -> None:
    from storage_engine import page_size_fanout_sweep

    # Sweep fanouts from order 4 to order 64
    orders = [4, 8, 16, 32, 64]
    sweep = page_size_fanout_sweep(n_keys=1000, orders=orders)

    # Higher fan-out (larger page size) strictly reduces tree depth
    assert sweep[4] > sweep[16] >= sweep[64]
    assert sweep[64] <= 3  # High-fanout B+ tree stays extremely shallow (< 4 I/O seeks for 1000 keys)


@pytest.mark.perf
def test_bplus_tree_lookup_scales_logarithmically() -> None:
    tree_small = BPlusTree(order=16)
    for i in range(100):
        tree_small.insert(i, RID(page_id=i // 10, slot_id=i % 10))

    tree_large = BPlusTree(order=16)
    for i in range(10_000):  # 100x larger
        tree_large.insert(i, RID(page_id=i // 10, slot_id=i % 10))

    # Height should grow only by a few levels (e.g. from 2-3 to 4-5) despite 100x data growth
    assert tree_large.height() <= tree_small.height() + 3

