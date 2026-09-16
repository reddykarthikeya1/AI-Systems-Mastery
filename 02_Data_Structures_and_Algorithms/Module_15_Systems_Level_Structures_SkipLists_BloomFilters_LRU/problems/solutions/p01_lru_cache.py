"""Reference solution — Problem 01: LRU Cache With O(1) Operations

Pattern:    Hash map + doubly linked list
Complexity: Time O(1) per operation, Space O(capacity)
"""

from __future__ import annotations


def simulate_lru(capacity: int, ops: list[tuple[str, int, int]]) -> list[int]:
    from collections import OrderedDict

    if capacity < 1:
        raise ValueError(f"capacity must be at least 1, got {capacity}")

    # OrderedDict is a hash map plus a doubly linked list, which is exactly the
    # structure this problem is about. Both operations below are O(1).
    cache: OrderedDict[int, int] = OrderedDict()
    out: list[int] = []

    for name, key, value in ops:
        if name == "get":
            if key in cache:
                cache.move_to_end(key)      # a hit is a use
                out.append(cache[key])
            else:
                out.append(-1)
        elif name == "put":
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)   # evict the least recently used
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
