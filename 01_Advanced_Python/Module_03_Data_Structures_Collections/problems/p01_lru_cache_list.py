"""Problem 01 — LRU Key Eviction Order

Target: Production-grade implementation

Example:
    >>> lru_cache_list(2, [('set', 'a'), ('set', 'b'), ('get', 'a'), ('set', 'c')])
    ['a', 'c']

Hints:
    Hint 1: You don't need to return values — only the final set of keys that
        are still cached, in order from least- to most-recently used.
    Hint 2: A regular dict already preserves insertion order, so use it as an
        ordered set: pop-then-reinsert a key to mark it "most recently used"
        on both 'get' and 'set' of an existing key.
    Hint 3: A 'get' on a key that isn't cached is a no-op (don't insert it),
        and eviction on 'set' only happens when the key is new AND the cache
        is already at capacity — evict `next(iter(cache))`, the oldest entry,
        before inserting the new one.
"""

from __future__ import annotations


def lru_cache_list(capacity: int, operations: list[tuple[str, str]]) -> list[str]:
    raise NotImplementedError('Implement lru_cache_list')
