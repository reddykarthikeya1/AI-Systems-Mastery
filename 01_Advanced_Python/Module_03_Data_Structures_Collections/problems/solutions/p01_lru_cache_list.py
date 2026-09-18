"""Problem 01 — LRU Key Eviction Order

Target: Production-grade implementation
"""

from __future__ import annotations


def lru_cache_list(capacity: int, operations: list[tuple[str, str]]) -> list[str]:
    cache = {}
    for op, key in operations:
        if op == 'get':
            if key in cache:
                val = cache.pop(key)
                cache[key] = val
        elif op == 'set':
            if key in cache:
                cache.pop(key)
            elif len(cache) >= capacity:
                oldest = next(iter(cache))
                cache.pop(oldest)
            cache[key] = True
    return list(cache.keys())
