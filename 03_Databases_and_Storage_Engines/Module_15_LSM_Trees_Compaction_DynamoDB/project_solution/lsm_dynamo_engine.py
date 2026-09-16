"""Module 15: LSM-Tree, Bloom Filter & DynamoDB Engine (Solution).

This is a pure-Python MODEL of LSM-Tree storage mechanics, Bloom filters, and DynamoDB's single-table design, built to make the
mechanism visible. It does not connect to AWS DynamoDB. For the real driver,
real queries and real operational behaviour, see `dynamo_live.py`.

Implements:
1. BloomFilter: Bit-array probabilistic filter with zero false negatives.
2. MemTable and SSTable: Sorted in-memory buffers and immutable on-disk tables with sparse indexing.
3. Leveled/Merge Compaction: Multi-way merge discarding obsolete versions and tombstones.
4. DynamoDBSingleTableEngine: PK/SK partition-sort queries and exact RCU/WCU cost accounting.
"""

from __future__ import annotations

import hashlib
import math
import time
from typing import Any


class BloomFilter:
    """Probabilistic data structure guaranteeing zero false negatives."""

    def __init__(self, expected_items: int = 100, false_positive_rate: float = 0.01) -> None:
        self.expected_items = max(1, expected_items)
        self.false_positive_rate = false_positive_rate
        # Calculate optimal bit array size: m = - (n * ln(p)) / (ln(2)^2)
        self.m = max(16, int(- (self.expected_items * math.log(self.false_positive_rate)) / (math.log(2) ** 2)))
        # Calculate optimal number of hash functions: k = (m / n) * ln(2)
        self.k = max(1, int((self.m / self.expected_items) * math.log(2)))
        self.bit_array = [0] * self.m

    def _hashes(self, item: str) -> list[int]:
        positions = []
        for i in range(self.k):
            seed = f"{item}:{i}".encode("utf-8")
            digest = int(hashlib.sha256(seed).hexdigest(), 16)
            positions.append(digest % self.m)
        return positions

    def add(self, item: str) -> None:
        for pos in self._hashes(item):
            self.bit_array[pos] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[pos] == 1 for pos in self._hashes(item))


class SSTable:
    """An immutable, sorted on-disk table with embedded Bloom filter and sparse index."""

    def __init__(self, entries: list[tuple[str, Any, int, bool]], sparse_interval: int = 2) -> None:
        # Sort entries strictly by key
        self.entries = sorted(entries, key=lambda x: x[0])
        self.sparse_interval = sparse_interval

        # Build embedded Bloom Filter
        self.bloom_filter = BloomFilter(expected_items=max(len(self.entries), 10), false_positive_rate=0.01)
        for key, _, _, _ in self.entries:
            self.bloom_filter.add(key)

        # Build Sparse Index: maps key to array index every sparse_interval items
        self.sparse_index: dict[str, int] = {}
        for idx in range(0, len(self.entries), self.sparse_interval):
            self.sparse_index[self.entries[idx][0]] = idx

    def get(self, key: str) -> tuple[Any, int, bool] | None:
        # Step 1: Bloom filter check. If False, key is guaranteed absent -> ZERO disk reads!
        if not self.bloom_filter.contains(key):
            return None

        # Step 2: Binary search on sorted entries
        low = 0
        high = len(self.entries) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_key = self.entries[mid][0]
            if mid_key == key:
                _, val, ts, is_tomb = self.entries[mid]
                return val, ts, is_tomb
            elif mid_key < key:
                low = mid + 1
            else:
                high = mid - 1

        return None


class MemTable:
    """In-memory sorted write buffer with flush threshold."""

    def __init__(self, max_entries: int = 4) -> None:
        self.max_entries = max_entries
        self.storage: dict[str, tuple[Any, int, bool]] = {}

    def is_full(self) -> bool:
        return len(self.storage) >= self.max_entries

    def put(self, key: str, value: Any, timestamp_us: int) -> None:
        self.storage[key] = (value, timestamp_us, False)

    def delete(self, key: str, timestamp_us: int) -> None:
        self.storage[key] = (None, timestamp_us, True)

    def flush(self) -> SSTable:
        entries = [(k, v[0], v[1], v[2]) for k, v in self.storage.items()]
        self.storage.clear()
        return SSTable(entries)


class LSMTreeEngine:
    """Log-Structured Merge-Tree coordinating MemTable, SSTables, and compaction."""

    def __init__(self, memtable_max_entries: int = 4) -> None:
        self.memtable = MemTable(max_entries=memtable_max_entries)
        # Newest SSTable at index 0, oldest at the end
        self.sstables: list[SSTable] = []

    def put(self, key: str, value: Any) -> None:
        timestamp_us = int(time.time() * 1_000_000)
        if self.memtable.is_full():
            self.sstables.insert(0, self.memtable.flush())
        self.memtable.put(key, value, timestamp_us)

    def delete(self, key: str) -> None:
        timestamp_us = int(time.time() * 1_000_000)
        if self.memtable.is_full():
            self.sstables.insert(0, self.memtable.flush())
        self.memtable.delete(key, timestamp_us)

    def get(self, key: str) -> Any | None:
        # Search 1: In-memory active MemTable
        if key in self.memtable.storage:
            val, _, is_tomb = self.memtable.storage[key]
            return None if is_tomb else val

        # Search 2: Disk SSTables from newest to oldest
        for sstable in self.sstables:
            res = sstable.get(key)
            if res is not None:
                val, _, is_tomb = res
                return None if is_tomb else val

        return None

    def compact(self) -> None:
        """Merge all SSTables into a single compacted SSTable, discarding stale versions & tombstones."""
        if not self.sstables:
            return

        # Multi-way merge: collect all keys across all SSTables
        latest_versions: dict[str, tuple[Any, int, bool]] = {}
        for sstable in reversed(self.sstables):  # Process oldest to newest
            for key, val, ts, is_tomb in sstable.entries:
                if key not in latest_versions or ts >= latest_versions[key][1]:
                    latest_versions[key] = (val, ts, is_tomb)

        # Discard tombstones during compaction
        alive_entries: list[tuple[str, Any, int, bool]] = []
        for key, (val, ts, is_tomb) in latest_versions.items():
            if not is_tomb:
                alive_entries.append((key, val, ts, is_tomb))

        self.sstables = [SSTable(alive_entries)] if alive_entries else []


class DynamoDBSingleTableEngine:
    """Simulates DynamoDB single-table design with PK, SK, and RCU/WCU accounting."""

    def __init__(self) -> None:
        self.store: dict[tuple[str, str], dict[str, Any]] = {}

    def put_item(self, item: dict[str, Any]) -> float:
        if "PK" not in item or "SK" not in item:
            raise ValueError("DynamoDB items require 'PK' and 'SK' attributes")

        key = (str(item["PK"]), str(item["SK"]))
        self.store[key] = dict(item)

        # 1 WCU per 1 KB
        item_size_bytes = len(str(item).encode("utf-8"))
        wcu = max(1.0, float(math.ceil(item_size_bytes / 1024.0)))
        return wcu

    def get_item(self, pk: str, sk: str, consistent_read: bool = False) -> tuple[dict[str, Any] | None, float]:
        key = (pk, sk)
        item = self.store.get(key)
        if item is None:
            # 1 RCU minimum for strong read, 0.5 for eventual
            return None, 1.0 if consistent_read else 0.5

        item_size_bytes = len(str(item).encode("utf-8"))
        # 1 RCU = 4 KB for strongly consistent read, 0.5 RCU for eventually consistent
        chunks_of_4kb = max(1, math.ceil(item_size_bytes / 4096.0))
        rcu = float(chunks_of_4kb) if consistent_read else chunks_of_4kb * 0.5
        return dict(item), rcu

    def query(self, pk: str, sk_prefix: str = "") -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for (item_pk, item_sk), val in sorted(self.store.items(), key=lambda x: x[0][1]):
            if item_pk == pk and item_sk.startswith(sk_prefix):
                results.append(dict(val))
        return results
