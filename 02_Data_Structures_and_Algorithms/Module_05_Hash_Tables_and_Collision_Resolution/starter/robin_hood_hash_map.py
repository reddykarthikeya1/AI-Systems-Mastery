"""Starter template for RobinHoodHashMap."""
from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class RobinHoodHashMap(Generic[K, V]):
    """Open-addressing hash table implementing Robin Hood hashing."""

    def __init__(self, initial_capacity: int = 16, max_load_factor: float = 0.75) -> None:
        raise NotImplementedError

    def put(self, key: K, val: V) -> None:
        raise NotImplementedError

    def get(self, key: K) -> V:
        raise NotImplementedError

    def remove(self, key: K) -> V:
        raise NotImplementedError

    def __contains__(self, key: K) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
