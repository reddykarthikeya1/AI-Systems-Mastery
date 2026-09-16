"""Production solution for MonotonicQueueEngine."""
from __future__ import annotations

from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")

class MinMaxStack(Generic[T]):
    """Stack with O(1) push, pop, min, and max via auxiliary tracking."""

    def __init__(self) -> None:
        self._stack: list[T] = []
        self._min_stack: list[T] = []
        self._max_stack: list[T] = []

    def push(self, val: T) -> None:
        self._stack.append(val)
        if not self._min_stack or val <= self._min_stack[-1]:
            self._min_stack.append(val)
        else:
            self._min_stack.append(self._min_stack[-1])

        if not self._max_stack or val >= self._max_stack[-1]:
            self._max_stack.append(val)
        else:
            self._max_stack.append(self._max_stack[-1])

    def pop(self) -> T:
        if not self._stack:
            raise IndexError("pop from empty stack")
        self._min_stack.pop()
        self._max_stack.pop()
        return self._stack.pop()

    def top(self) -> T:
        if not self._stack:
            raise IndexError("top from empty stack")
        return self._stack[-1]

    def get_min(self) -> T:
        if not self._min_stack:
            raise IndexError("min of empty stack")
        return self._min_stack[-1]

    def get_max(self) -> T:
        if not self._max_stack:
            raise IndexError("max of empty stack")
        return self._max_stack[-1]

    def __len__(self) -> int:
        return len(self._stack)


class MonotonicQueue:
    """Monotonic decreasing deque supporting sliding window maximum in O(1) amortized."""

    def __init__(self) -> None:
        self._deque: deque[int] = deque()

    def push(self, val: int) -> None:
        """Push val, maintaining monotonic decreasing order by evicting smaller elements."""
        while self._deque and self._deque[-1] < val:
            self._deque.pop()
        self._deque.append(val)

    def pop(self, val: int) -> None:
        """Pop val if it is currently at the front of the window."""
        if self._deque and self._deque[0] == val:
            self._deque.popleft()

    def max(self) -> int:
        """Return maximum value in the current window."""
        if not self._deque:
            raise IndexError("max from empty monotonic queue")
        return self._deque[0]

    def __len__(self) -> int:
        return len(self._deque)
