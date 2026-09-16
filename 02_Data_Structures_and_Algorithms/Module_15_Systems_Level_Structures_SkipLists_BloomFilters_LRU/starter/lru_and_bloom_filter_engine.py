"""Starter template for LRUAndBloomFilterEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class LRUCache(Generic[K, V]):
    """O(1) Least Recently Used cache with DLL + Hash Map."""
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: K) -> V:
        raise NotImplementedError

    def put(self, key: K, val: V) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class BloomFilter:
    """Probabilistic set membership filter."""
    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01) -> None:
        raise NotImplementedError

    def add(self, item: str) -> None:
        raise NotImplementedError

    def contains(self, item: str) -> bool:
        """Returns True if possibly present, False if definitely absent."""
        raise NotImplementedError
