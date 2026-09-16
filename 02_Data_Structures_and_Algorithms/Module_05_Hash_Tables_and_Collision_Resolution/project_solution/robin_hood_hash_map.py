"""Production solution for RobinHoodHashMap."""
from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class Entry(Generic[K, V]):
    __slots__ = ("key", "psl", "val")
    def __init__(self, key: K, val: V, psl: int = 0):
        self.key = key
        self.val = val
        self.psl = psl  # Probe Sequence Length

class RobinHoodHashMap(Generic[K, V]):
    """Robin Hood hash map with linear probing and backward-shift deletion."""

    def __init__(self, initial_capacity: int = 16, max_load_factor: float = 0.75) -> None:
        self._capacity = max(initial_capacity, 4)
        self._max_load = max_load_factor
        self._size = 0
        self._buckets: list[Entry[K, V] | None] = [None] * self._capacity

    def _hash(self, key: K) -> int:
        return hash(key) & 0x7FFFFFFF % self._capacity

    def put(self, key: K, val: V) -> None:
        if (self._size + 1) / self._capacity >= self._max_load:
            self._resize(self._capacity * 2)

        idx = self._hash(key)
        new_entry = Entry[K, V](key, val, 0)

        while True:
            curr = self._buckets[idx]
            if curr is None:
                self._buckets[idx] = new_entry
                self._size += 1
                return

            if curr.key == key:
                curr.val = val  # Update existing key
                return

            # Robin Hood heuristic: Rich gives to poor
            if curr.psl < new_entry.psl:
                self._buckets[idx] = new_entry
                new_entry = curr

            new_entry.psl += 1
            idx = (idx + 1) % self._capacity

    def get(self, key: K) -> V:
        idx = self._hash(key)
        dist = 0
        while True:
            curr = self._buckets[idx]
            if curr is None or dist > curr.psl:
                raise KeyError(f"Key not found: {key}")
            if curr.key == key:
                return curr.val
            dist += 1
            idx = (idx + 1) % self._capacity

    def remove(self, key: K) -> V:
        idx = self._hash(key)
        dist = 0
        while True:
            curr = self._buckets[idx]
            if curr is None or dist > curr.psl:
                raise KeyError(f"Key not found: {key}")
            if curr.key == key:
                val = curr.val
                self._buckets[idx] = None
                self._size -= 1
                # Backward-shift deletion to preserve PSL invariant
                self._backward_shift(idx)
                return val
            dist += 1
            idx = (idx + 1) % self._capacity

    def _backward_shift(self, start_idx: int) -> None:
        curr_idx = (start_idx + 1) % self._capacity
        target_idx = start_idx
        while True:
            curr = self._buckets[curr_idx]
            if curr is None or curr.psl == 0:
                break
            curr.psl -= 1
            self._buckets[target_idx] = curr
            self._buckets[curr_idx] = None
            target_idx = curr_idx
            curr_idx = (curr_idx + 1) % self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * self._capacity
        self._size = 0
        for entry in old_buckets:
            if entry is not None:
                self.put(entry.key, entry.val)

    def __contains__(self, key: K) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity
