"""Starter template for DoublyLinkedListEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, val: T, prev: Node[T] | None = None, next_node: Node[T] | None = None):
        self.val = val
        self.prev = prev
        self.next = next_node

class DoublyLinkedListEngine(Generic[T]):
    """Sentinel-based Doubly Linked List engine."""

    def __init__(self) -> None:
        raise NotImplementedError

    def push_front(self, val: T) -> None:
        raise NotImplementedError

    def push_back(self, val: T) -> None:
        raise NotImplementedError

    def pop_front(self) -> T:
        raise NotImplementedError

    def pop_back(self) -> T:
        raise NotImplementedError

    def reverse(self) -> None:
        """In-place pointer reversal."""
        raise NotImplementedError

    def has_cycle(self) -> bool:
        """Floyd's Tortoise and Hare cycle detection."""
        raise NotImplementedError

    def to_list(self) -> list[T]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
