"""Starter template for MonotonicQueueEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class MinMaxStack(Generic[T]):
    """Stack supporting O(1) push, pop, min, and max."""
    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, val: T) -> None:
        raise NotImplementedError

    def pop(self) -> T:
        raise NotImplementedError

    def top(self) -> T:
        raise NotImplementedError

    def get_min(self) -> T:
        raise NotImplementedError

    def get_max(self) -> T:
        raise NotImplementedError

class MonotonicQueue:
    """Monotonic Decreasing Deque for Sliding Window Maximum in O(1) amortized."""
    def __init__(self) -> None:
        raise NotImplementedError

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self, val: int) -> None:
        raise NotImplementedError

    def max(self) -> int:
        raise NotImplementedError
