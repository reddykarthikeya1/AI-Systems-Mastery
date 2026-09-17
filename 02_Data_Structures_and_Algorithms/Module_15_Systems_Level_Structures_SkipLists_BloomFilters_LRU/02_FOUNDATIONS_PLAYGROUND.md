# 🐣 Interactive Foundations Playground: Systems Structures: LRU Cache & Bloom Filter

> *"An LRU cache is a desktop where frequently used books stay near your hand, and neglected books get packed into boxes."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import OrderedDict
import hashlib
```

---

## 1. LRU Cache Eviction Policy

An LRU cache evicts the least recently accessed item when capacity is exceeded, executing get and put in $O(1)$ time using a hash map and doubly-linked list.

```python
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
```

---

## 2. Bloom Filter Probabilistic Set Membership

A Bloom filter uses $k$ independent hash functions over an $M$-bit array: zero false negatives (if it says absent, it's definitely absent).

```python
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
```

---

## 3. Skip List Probabilistic Multi-Level Search

A skip list layers sparse express lanes over a linked list; coin flips determine height, achieving $O(\log N)$ average search.

```python
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
```

---
