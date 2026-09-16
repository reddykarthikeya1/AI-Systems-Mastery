"""Production reference implementation of DynamicArrayEngine."""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class DynamicArrayEngine(Generic[T]):
    """An industrial-grade, cache-conscious dynamic array with automated compaction."""

    def __init__(self, initial_capacity: int = 4) -> None:
        self._size: int = 0
        self._capacity: int = max(1, initial_capacity)
        self._buffer: list[T | None] = [None] * self._capacity
        self.reallocation_count: int = 0

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def _resize(self, new_capacity: int) -> None:
        new_buffer: list[T | None] = [None] * new_capacity
        for i in range(self._size):
            new_buffer[i] = self._buffer[i]
        self._buffer = new_buffer
        self._capacity = new_capacity
        self.reallocation_count += 1

    def __getitem__(self, index: int) -> T:
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")
        val = self._buffer[index]
        return val  # type: ignore[return-value]

    def __setitem__(self, index: int, value: T) -> None:
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")
        self._buffer[index] = value

    def append(self, item: T) -> None:
        """Append item in O(1) amortized time, doubling capacity when full."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._buffer[self._size] = item
        self._size += 1

    def pop(self) -> T:
        """Pop item from end in O(1) amortized time, halving capacity when <= 25% full."""
        if self._size == 0:
            raise IndexError("Cannot pop from an empty dynamic array")
        self._size -= 1
        val = self._buffer[self._size]
        self._buffer[self._size] = None

        if self._capacity > 8 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)

        return val  # type: ignore[return-value]

    def to_list(self) -> list[T]:
        return [self[i] for i in range(self._size)]

    def reverse_in_place(self) -> None:
        """Reverse elements in-place with O(1) auxiliary memory using two pointers."""
        left, right = 0, self._size - 1
        while left < right:
            self._buffer[left], self._buffer[right] = self._buffer[right], self._buffer[left]
            left += 1
            right -= 1

    def max_sliding_window_sum(self, k: int) -> int:
        """Find max sum of contiguous subarray of size k in O(N) time."""
        if k <= 0 or k > self._size:
            raise ValueError("Window size k must be between 1 and size")
        window_sum = sum(self[i] for i in range(k))  # type: ignore
        max_sum = window_sum
        for i in range(k, self._size):
            window_sum += self[i] - self[i - k]  # type: ignore
            max_sum = max(max_sum, window_sum)
        return max_sum

    def prefix_sums(self) -> list[int]:
        """Compute running prefix sums array in O(N) time."""
        res = [0] * (self._size + 1)
        for i in range(self._size):
            res[i + 1] = res[i] + self[i]  # type: ignore
        return res
