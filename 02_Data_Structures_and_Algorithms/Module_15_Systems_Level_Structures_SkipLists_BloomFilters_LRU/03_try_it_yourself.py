"""Beginner playground for Module 15 - Systems Structures: LRU Cache & Bloom Filter.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import OrderedDict
import hashlib

# -------------------------------------------- 1. LRU Cache Eviction Policy
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()
    def get(self, key: str) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    def put(self, key: str, val: int):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = val
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)

lru = LRUCache(2)
lru.put("A", 1)
lru.put("B", 2)
assert lru.get("A") == 1, "Accessing 'A' marks it most recently used"
lru.put("C", 3)  # Evicts 'B', not 'A'
assert lru.get("B") == -1, "'B' must be evicted"
assert lru.get("C") == 3
print("LRU cache properly evicted least-recently used entry.")

# -------------------------------------------- 2. Bloom Filter Probabilistic Set Membership
class SimpleBloomFilter:
    def __init__(self, size=64):
        self.size = size
        self.bits = [0] * size
    def _hashes(self, item):
        h1 = hash(item) & 0x7FFFFFFF % self.size
        h2 = (hash(item) * 31 + 7) & 0x7FFFFFFF % self.size
        return [h1, h2]
    def add(self, item):
        for h in self._hashes(item):
            self.bits[h] = 1
    def contains(self, item):
        return all(self.bits[h] == 1 for h in self._hashes(item))

bf = SimpleBloomFilter(64)
bf.add("user_101")
bf.add("user_102")
assert bf.contains("user_101") is True
assert bf.contains("user_102") is True
assert bf.contains("unknown_user_999") is False
print("Bloom filter membership queries confirmed.")

# -------------------------------------------- 3. Skip List Probabilistic Multi-Level Search
import random
random.seed(42)
def coin_flip_height(max_height=4):
    h = 1
    while h < max_height and random.random() < 0.5:
        h += 1
    return h

heights = [coin_flip_height() for _ in range(100)]
assert all(1 <= h <= 4 for h in heights)
assert any(h > 1 for h in heights), "Express lane towers created"
print(f"Simulated tower heights distribution: min={min(heights)}, max={max(heights)}")

print()
print("All checks passed.")
