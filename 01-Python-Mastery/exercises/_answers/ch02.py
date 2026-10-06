"""Chapter 02 - Data structures under the hood.

1. LRUCache: O(1) get/put with least-recently-used eviction.
2. top_k_frequent: heap or counter based top-k with deterministic tie-breaking.
3. dedupe_keep_order (debugging): removes duplicates but scrambles the order.
"""
import heapq
from collections import Counter, OrderedDict

BUGGY = {
    "dedupe_keep_order": '''def dedupe_keep_order(items):
    """Remove duplicates from a list of hashable items, keeping the first occurrence of each in original order."""
    return list(set(items))''',
}


class LRUCache:
    """Fixed-capacity cache. get(key) returns the value or None and marks the key most recently used.
    put(key, value) inserts or updates and evicts the least recently used key when over capacity.
    capacity must be >= 1 (ValueError otherwise). Both operations must be O(1)."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._d = OrderedDict()

    def get(self, key):
        if key not in self._d:
            return None
        self._d.move_to_end(key)
        return self._d[key]

    def put(self, key, value):
        self._d[key] = value
        self._d.move_to_end(key)
        if len(self._d) > self.capacity:
            self._d.popitem(last=False)

    def __len__(self):
        return len(self._d)


def top_k_frequent(words, k):
    """Return the k most frequent words, most frequent first; ties broken alphabetically.
    Must run in O(n log k), not O(n log n). Return fewer than k if there are fewer distinct words."""
    counts = Counter(words)
    return [w for w, _ in heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def dedupe_keep_order(items):
    """Remove duplicates from a list of hashable items, keeping the first occurrence of each in original order."""
    return list(dict.fromkeys(items))


def t_lru_eviction_order(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") is None and c.get("a") == 1 and c.get("c") == 3
    assert len(c) == 2


def t_lru_update_and_capacity(m):
    c = m.LRUCache(1)
    c.put("a", 1)
    c.put("a", 2)
    assert c.get("a") == 2 and len(c) == 1
    c.put("b", 3)
    assert c.get("a") is None
    try:
        m.LRUCache(0)
    except ValueError:
        return
    raise AssertionError("capacity 0 must raise")


def t_top_k_ties_and_short(m):
    words = "b a c a b d".split()
    assert m.top_k_frequent(words, 2) == ["a", "b"]
    assert m.top_k_frequent(words, 10) == ["a", "b", "c", "d"]
    assert m.top_k_frequent([], 3) == []


def t_top_k_scales(m):
    import time
    words = [str(i % 5000) for i in range(300_000)]
    t0 = time.perf_counter()
    assert len(m.top_k_frequent(words, 3)) == 3
    assert time.perf_counter() - t0 < 2.0


def t_dedupe_order(m):
    assert m.dedupe_keep_order([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert m.dedupe_keep_order(list("banana")) == ["b", "a", "n"]
    assert m.dedupe_keep_order([]) == []
