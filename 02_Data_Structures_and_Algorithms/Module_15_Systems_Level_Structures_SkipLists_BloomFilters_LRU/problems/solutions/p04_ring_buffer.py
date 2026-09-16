"""Reference solution — Problem 04: Fixed-Capacity Ring Buffer

Pattern:    Circular buffer
Complexity: Time O(1) per operation, Space O(capacity)
"""

from __future__ import annotations


def simulate_ring_buffer(capacity: int, ops: list[tuple[str, int]]) -> list[int | None | list[int]]:
    if capacity < 1:
        raise ValueError(f"capacity must be at least 1, got {capacity}")

    buf: list[int] = [0] * capacity
    head = 0        # index of the oldest element
    count = 0
    out: list[int | None | list[int]] = []

    for name, value in ops:
        if name == "push":
            buf[(head + count) % capacity] = value
            if count < capacity:
                count += 1
            else:
                # Full: the write overwrote the oldest, so the head moves too.
                head = (head + 1) % capacity
        elif name == "pop":
            if count == 0:
                out.append(None)
            else:
                out.append(buf[head])
                head = (head + 1) % capacity
                count -= 1
        elif name == "items":
            out.append([buf[(head + i) % capacity] for i in range(count)])
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
