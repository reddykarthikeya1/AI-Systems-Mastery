"""Starter template for BinaryMinHeapEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class BinaryMinHeap(Generic[T]):
    """Array-backed Binary Min-Heap."""

    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, val: T) -> None:
        raise NotImplementedError

    def pop(self) -> T:
        raise NotImplementedError

    def peek(self) -> T:
        raise NotImplementedError

    @classmethod
    def heapify(cls, items: list[T]) -> BinaryMinHeap[T]:
        """Build heap in O(N) bottom-up time."""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class TopKTracker:
    """Track Top-K largest elements in streaming data in O(N log K)."""
    def __init__(self, k: int) -> None:
        raise NotImplementedError

    def add(self, val: int) -> None:
        raise NotImplementedError

    def get_top_k(self) -> list[int]:
        raise NotImplementedError
