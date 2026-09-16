"""Reference solution — Problem 05: LFU Cache

Pattern:    Frequency buckets
Complexity: Time O(1) per operation, Space O(capacity)
"""

from __future__ import annotations


def simulate_lfu(capacity: int, ops: list[tuple[str, int, int]]) -> list[int]:
    from collections import OrderedDict, defaultdict

    if capacity < 1:
        raise ValueError(f"capacity must be at least 1, got {capacity}")

    values: dict[int, int] = {}
    freq: dict[int, int] = {}
    # frequency -> keys at that frequency, least recently used first.
    buckets: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
    min_freq = 0
    out: list[int] = []

    def touch(key: int) -> None:
        nonlocal min_freq
        f = freq[key]
        del buckets[f][key]
        if not buckets[f]:
            del buckets[f]
            # Tracked incrementally so eviction never has to scan.
            if min_freq == f:
                min_freq = f + 1
        freq[key] = f + 1
        buckets[f + 1][key] = None

    for name, key, value in ops:
        if name == "get":
            if key in values:
                touch(key)
                out.append(values[key])
            else:
                out.append(-1)
        elif name == "put":
            if key in values:
                values[key] = value
                touch(key)
            else:
                if len(values) >= capacity:
                    # Least frequent, and least recent among those.
                    evict, _ = buckets[min_freq].popitem(last=False)
                    if not buckets[min_freq]:
                        del buckets[min_freq]
                    del values[evict]
                    del freq[evict]
                values[key] = value
                freq[key] = 1
                buckets[1][key] = None
                min_freq = 1        # the new key is the least frequent
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
