"""Production solution for DoublyLinkedListEngine."""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, val: T, prev: Node[T] | None = None, next_node: Node[T] | None = None):
        self.val = val
        self.prev = prev
        self.next = next_node

class DoublyLinkedListEngine(Generic[T]):
    """Sentinel-based Doubly Linked List engine with O(1) ends and in-place reversal."""

    def __init__(self) -> None:
        self._head: Node[Any] = Node(None)  # Sentinel head
        self._tail: Node[Any] = Node(None)  # Sentinel tail
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def push_front(self, val: T) -> None:
        first = self._head.next
        new_node = Node(val, prev=self._head, next_node=first)
        self._head.next = new_node
        if first:
            first.prev = new_node
        self._size += 1

    def push_back(self, val: T) -> None:
        last = self._tail.prev
        new_node = Node(val, prev=last, next_node=self._tail)
        if last:
            last.next = new_node
        self._tail.prev = new_node
        self._size += 1

    def pop_front(self) -> T:
        if self._size == 0:
            raise IndexError("pop from empty list")
        target = self._head.next
        assert target is not None and target is not self._tail
        nxt = target.next
        self._head.next = nxt
        if nxt:
            nxt.prev = self._head
        self._size -= 1
        return target.val

    def pop_back(self) -> T:
        if self._size == 0:
            raise IndexError("pop from empty list")
        target = self._tail.prev
        assert target is not None and target is not self._head
        prev = target.prev
        self._tail.prev = prev
        if prev:
            prev.next = self._tail
        self._size -= 1
        return target.val

    def reverse(self) -> None:
        """In-place pointer reversal swapping next and prev pointers."""
        if self._size <= 1:
            return

        curr: Node[Any] | None = self._head
        while curr:
            curr.prev, curr.next = curr.next, curr.prev
            curr = curr.prev  # Because we swapped, curr.prev is the original curr.next

        # Swap head and tail sentinel references
        self._head, self._tail = self._tail, self._head

    def has_cycle(self) -> bool:
        """Floyd's Tortoise and Hare cycle detection."""
        slow: Node[Any] | None = self._head.next
        fast: Node[Any] | None = self._head.next
        while fast and fast.next and fast is not self._tail and fast.next is not self._tail:
            slow = slow.next if slow else None
            fast = fast.next.next
            if slow is not None and slow is fast:
                return True
        return False

    def to_list(self) -> list[T]:
        res: list[T] = []
        curr = self._head.next
        while curr and curr is not self._tail:
            res.append(curr.val)
            curr = curr.next
        return res

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        curr = self._head.next
        while curr and curr is not self._tail:
            yield curr.val
            curr = curr.next
