"""Production solution for LRUAndBloomFilterEngine."""
from __future__ import annotations

import hashlib
import math
from typing import Any, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class DNode(Generic[K, V]):
    __slots__ = ("key", "next", "prev", "val")
    def __init__(self, key: Any, val: Any):
        self.key = key
        self.val = val
        self.prev: DNode[K, V] | None = None
        self.next: DNode[K, V] | None = None

class LRUCache(Generic[K, V]):
    """Thread-safe O(1) LRU Cache with Sentinel Doubly Linked List."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache: dict[K, DNode[K, V]] = {}
        # Sentinels
        self.head: DNode[K, V] = DNode(None, None)
        self.tail: DNode[K, V] = DNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DNode[K, V]) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _add_to_front(self, node: DNode[K, V]) -> None:
        first = self.head.next
        node.prev = self.head
        node.next = first
        self.head.next = node
        if first:
            first.prev = node

    def get(self, key: K) -> V:
        if key not in self.cache:
            raise KeyError(f"Key not found: {key}")
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: K, val: V) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict least recently used (node before tail)
            lru = self.tail.prev
            assert lru is not None and lru is not self.head
            self._remove(lru)
            del self.cache[lru.key]

        new_node = DNode(key, val)
        self.cache[key] = new_node
        self._add_to_front(new_node)

    def __len__(self) -> int:
        return len(self.cache)


class BloomFilter:
    """Probabilistic membership tester using double-hashing (Kirsch-Mitzenmacher)."""

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01) -> None:
        if expected_elements <= 0 or not (0 < false_positive_rate < 1):
            raise ValueError("Invalid parameters for BloomFilter")

        # Optimal bit array size m = - (n * ln(p)) / (ln 2)^2
        self.size = int(- (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2))
        # Optimal number of hash functions k = (m / n) * ln 2
        self.hash_count = max(1, int((self.size / expected_elements) * math.log(2)))
        self.bit_array = bytearray((self.size + 7) // 8)

    def _hashes(self, item: str) -> list[int]:
        """Generate k distinct hash indices using md5 and sha1."""
        h1 = int(hashlib.md5(item.encode("utf-8")).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode("utf-8")).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.hash_count)]

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            byte_idx = idx // 8
            bit_mask = 1 << (idx % 8)
            self.bit_array[byte_idx] |= bit_mask

    def contains(self, item: str) -> bool:
        """Never false negative: if False, item is definitely not in set."""
        for idx in self._hashes(item):
            byte_idx = idx // 8
            bit_mask = 1 << (idx % 8)
            if not (self.bit_array[byte_idx] & bit_mask):
                return False
        return True
