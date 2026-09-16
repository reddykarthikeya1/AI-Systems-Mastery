"""Module 21: Storage Engine Internals — Slotted Pages, Buffer Pool & B+ Tree (Solution).

Implements:
1. SlottedPage binary layout packing variable-length records with stable RIDs.
2. DiskManager simulating raw page block persistence.
3. BufferPoolManager coordinating frame pinning, dirty tracking, and CLOCK eviction.
4. BPlusTree with balanced node splitting, point lookups, and leaf-chained range scans.
"""

from __future__ import annotations

import struct
from typing import Any


class RID:
    """Record Identifier uniquely locating a tuple by Page ID and Slot ID."""

    def __init__(self, page_id: int, slot_id: int) -> None:
        self.page_id = page_id
        self.slot_id = slot_id

    def __repr__(self) -> str:
        return f"RID(page={self.page_id}, slot={self.slot_id})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RID):
            return False
        return self.page_id == other.page_id and self.slot_id == other.slot_id


class SlottedPage:
    """Fixed-size binary page storing variable-length tuples with lower/upper offsets."""

    HEADER_SIZE = 16
    SLOT_SIZE = 4

    def __init__(self, page_id: int, page_size: int = 4096, initial_data: bytearray | None = None) -> None:
        self.page_id = page_id
        self.page_size = page_size

        if initial_data is not None:
            self.data = bytearray(initial_data)
        else:
            self.data = bytearray(page_size)
            # Header layout:
            # bytes 0..2: tuple_count (0)
            # bytes 2..4: lower_offset (starts right after header = 16)
            # bytes 4..6: upper_offset (starts at end of page = page_size)
            struct.pack_into(">HHH", self.data, 0, 0, self.HEADER_SIZE, page_size)

    @property
    def tuple_count(self) -> int:
        return struct.unpack_from(">H", self.data, 0)[0]

    @property
    def lower_offset(self) -> int:
        return struct.unpack_from(">H", self.data, 2)[0]

    @property
    def upper_offset(self) -> int:
        return struct.unpack_from(">H", self.data, 4)[0]

    def _set_header(self, tuple_count: int, lower_offset: int, upper_offset: int) -> None:
        struct.pack_into(">HHH", self.data, 0, tuple_count, lower_offset, upper_offset)

    def free_space(self) -> int:
        return self.upper_offset - self.lower_offset

    def insert_tuple(self, payload: bytes) -> int | None:
        needed_space = self.SLOT_SIZE + len(payload)
        if self.free_space() < needed_space:
            return None

        # Write tuple at upper end
        new_upper = self.upper_offset - len(payload)
        self.data[new_upper : self.upper_offset] = payload

        # Write slot entry at lower offset: (offset, length)
        slot_id = self.tuple_count
        struct.pack_into(">HH", self.data, self.lower_offset, new_upper, len(payload))

        new_lower = self.lower_offset + self.SLOT_SIZE
        self._set_header(slot_id + 1, new_lower, new_upper)
        return slot_id

    def get_tuple(self, slot_id: int) -> bytes | None:
        if slot_id < 0 or slot_id >= self.tuple_count:
            return None

        slot_pos = self.HEADER_SIZE + slot_id * self.SLOT_SIZE
        offset, length = struct.unpack_from(">HH", self.data, slot_pos)
        return bytes(self.data[offset : offset + length])


class DiskManager:
    """Emulates on-disk page block allocation, reads, and writes."""

    def __init__(self, page_size: int = 4096) -> None:
        self.page_size = page_size
        self.pages: dict[int, bytearray] = {}
        self.next_page_id = 0

    def allocate_page(self) -> int:
        pid = self.next_page_id
        self.next_page_id += 1
        page = SlottedPage(page_id=pid, page_size=self.page_size)
        self.pages[pid] = bytearray(page.data)
        return pid

    def read_page(self, page_id: int) -> bytearray:
        if page_id not in self.pages:
            raise KeyError(f"Page {page_id} does not exist on disk")
        return bytearray(self.pages[page_id])

    def write_page(self, page_id: int, data: bytearray) -> None:
        self.pages[page_id] = bytearray(data)


class BufferPoolManager:
    """Coordinates memory frame caching, pin-count invariants, and CLOCK eviction."""

    def __init__(self, pool_size: int, disk_manager: DiskManager) -> None:
        self.pool_size = pool_size
        self.disk_manager = disk_manager

        self.frames: list[SlottedPage | None] = [None] * pool_size
        self.page_table: dict[int, int] = {}  # page_id -> frame_id
        self.pin_counts: list[int] = [0] * pool_size
        self.is_dirty: list[bool] = [False] * pool_size
        self.clock_refs: list[int] = [0] * pool_size
        self.clock_hand: int = 0

    def _find_evict_frame(self) -> int:
        # Check for free frames first
        for i in range(self.pool_size):
            if self.frames[i] is None:
                return i

        # CLOCK (Second-Chance) replacement algorithm
        attempts = 0
        while attempts < self.pool_size * 2:
            frame_id = self.clock_hand
            self.clock_hand = (self.clock_hand + 1) % self.pool_size

            if self.pin_counts[frame_id] == 0:
                if self.clock_refs[frame_id] == 1:
                    self.clock_refs[frame_id] = 0
                else:
                    return frame_id

            attempts += 1

        raise RuntimeError("BufferPoolManager Error: All frames are pinned! Cannot evict.")

    def fetch_page(self, page_id: int) -> SlottedPage:
        # 1. Page already in memory frame
        if page_id in self.page_table:
            frame_id = self.page_table[page_id]
            self.pin_counts[frame_id] += 1
            self.clock_refs[frame_id] = 1
            page = self.frames[frame_id]
            assert page is not None
            return page

        # 2. Must load from disk into a frame
        frame_id = self._find_evict_frame()
        old_page = self.frames[frame_id]

        # Flush old page if dirty
        if old_page is not None:
            if self.is_dirty[frame_id]:
                self.disk_manager.write_page(old_page.page_id, old_page.data)
            del self.page_table[old_page.page_id]

        # Read page data from disk
        raw_data = self.disk_manager.read_page(page_id)
        new_page = SlottedPage(page_id=page_id, page_size=len(raw_data), initial_data=raw_data)

        self.frames[frame_id] = new_page
        self.page_table[page_id] = frame_id
        self.pin_counts[frame_id] = 1
        self.is_dirty[frame_id] = False
        self.clock_refs[frame_id] = 1

        return new_page

    def unpin_page(self, page_id: int, is_dirty: bool = False) -> bool:
        if page_id not in self.page_table:
            return False

        frame_id = self.page_table[page_id]
        if self.pin_counts[frame_id] > 0:
            self.pin_counts[frame_id] -= 1

        if is_dirty:
            self.is_dirty[frame_id] = True

        return True

    def flush_page(self, page_id: int) -> None:
        if page_id in self.page_table:
            frame_id = self.page_table[page_id]
            page = self.frames[frame_id]
            if page is not None:
                self.disk_manager.write_page(page_id, page.data)
                self.is_dirty[frame_id] = False


class BPlusTreeNode:
    """Node in the B+ Tree."""

    def __init__(self, is_leaf: bool = False) -> None:
        self.is_leaf = is_leaf
        self.keys: list[int] = []
        # For leaf: list[RID]. For internal: list[BPlusTreeNode]
        self.children: list[Any] = []
        self.next_leaf: BPlusTreeNode | None = None


class BPlusTree:
    """Self-balancing B+ Tree with internal routing and doubly-linked leaves."""

    def __init__(self, order: int = 3) -> None:
        self.order = max(3, order)
        self.root = BPlusTreeNode(is_leaf=True)

    def search(self, key: int) -> RID | None:
        curr = self.root
        while not curr.is_leaf:
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]

        for i, k in enumerate(curr.keys):
            if k == key:
                return curr.children[i]
        return None

    def insert(self, key: int, rid: RID) -> None:
        root = self.root
        # If root is full, split root
        if len(root.keys) >= self.order:
            new_root = BPlusTreeNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, rid)

    def _insert_non_full(self, node: BPlusTreeNode, key: int, rid: RID) -> None:
        if node.is_leaf:
            # Insert into sorted position
            idx = 0
            while idx < len(node.keys) and node.keys[idx] < key:
                idx += 1
            node.keys.insert(idx, key)
            node.children.insert(idx, rid)
        else:
            # Find child to recurse into
            idx = len(node.keys) - 1
            while idx >= 0 and key < node.keys[idx]:
                idx -= 1
            idx += 1

            if len(node.children[idx].keys) >= self.order:
                self._split_child(node, idx)
                if key >= node.keys[idx]:
                    idx += 1

            self._insert_non_full(node.children[idx], key, rid)

    def _split_child(self, parent: BPlusTreeNode, index: int) -> None:
        child = parent.children[index]
        mid = len(child.keys) // 2

        new_child = BPlusTreeNode(is_leaf=child.is_leaf)

        if child.is_leaf:
            # Leaf split: copy middle key to parent, preserve in right child
            push_key = child.keys[mid]
            new_child.keys = child.keys[mid:]
            new_child.children = child.children[mid:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid]

            new_child.next_leaf = child.next_leaf
            child.next_leaf = new_child
        else:
            # Internal split: move middle key to parent
            push_key = child.keys[mid]
            new_child.keys = child.keys[mid + 1 :]
            new_child.children = child.children[mid + 1 :]
            child.keys = child.keys[:mid]
            child.children = child.children[: mid + 1]

        parent.keys.insert(index, push_key)
        parent.children.insert(index + 1, new_child)

    def range_scan(self, min_key: int, max_key: int) -> list[tuple[int, RID]]:
        results: list[tuple[int, RID]] = []

        # Find lower bound leaf in O(log N)
        curr = self.root
        while not curr.is_leaf:
            idx = 0
            while idx < len(curr.keys) and min_key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]

        # Scan forward along leaf pointers in O(1)
        done = False
        while curr is not None and not done:
            for i, k in enumerate(curr.keys):
                if k >= min_key:
                    if k <= max_key:
                        results.append((k, curr.children[i]))
                    else:
                        done = True
                        break
            curr = curr.next_leaf

        return results

    def height(self) -> int:
        """Calculates the current depth/height of the B+ Tree from root to leaf."""
        h = 1
        curr = self.root
        while not curr.is_leaf:
            if not curr.children:
                break
            curr = curr.children[0]
            h += 1
        return h


def page_size_fanout_sweep(n_keys: int = 5000, orders: list[int] | None = None) -> dict[int, int]:
    """Sweeps over different B+ Tree fanout orders to demonstrate tree depth reduction.

    A larger page size accommodates higher order (fan-out), dramatically reducing tree depth
    and thus disk I/O seek operations.
    """
    if orders is None:
        orders = [4, 8, 16, 32, 64]

    depth_by_order: dict[int, int] = {}
    for ord_val in orders:
        tree = BPlusTree(order=ord_val)
        for i in range(n_keys):
            tree.insert(i, RID(page_id=i // 100, slot_id=i % 100))
        depth_by_order[ord_val] = tree.height()

    return depth_by_order

