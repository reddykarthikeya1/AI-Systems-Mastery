"""Production solution for BinaryMinHeapEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class BinaryMinHeap(Generic[T]):
    """Array-backed Binary Min-Heap with O(log N) push/pop and O(N) heapify."""

    def __init__(self) -> None:
        self._heap: list[T] = []

    def push(self, val: T) -> None:
        self._heap.append(val)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> T:
        if not self._heap:
            raise IndexError("pop from empty heap")
        min_val = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return min_val

    def peek(self) -> T:
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break

    @classmethod
    def heapify(cls, items: list[T]) -> BinaryMinHeap[T]:
        """Bottom-up heap construction in O(N) time."""
        h = cls()
        h._heap = list(items)
        n = len(h._heap)
        for i in range(n // 2 - 1, -1, -1):
            h._sift_down(i)
        return h

    def __len__(self) -> int:
        return len(self._heap)


class TopKTracker:
    """Stream Top-K largest numbers maintaining min-heap of size K."""

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("k must be positive")
        self.k = k
        self.heap = BinaryMinHeap[int]()

    def add(self, val: int) -> None:
        if len(self.heap) < self.k:
            self.heap.push(val)
        elif val > self.heap.peek():
            self.heap.pop()
            self.heap.push(val)

    def get_top_k(self) -> list[int]:
        # Return sorted descending
        elements = list(self.heap._heap)
        return sorted(elements, reverse=True)
