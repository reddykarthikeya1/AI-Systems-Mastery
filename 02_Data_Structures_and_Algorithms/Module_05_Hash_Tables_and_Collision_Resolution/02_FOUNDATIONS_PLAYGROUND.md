# 🐣 Interactive Foundations Playground: Hash Tables & Collision Resolution

> *"A hash table is an organizer with labelled pigeonholes: hash the key to pick the slot."*

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
import hashlib
```

---

## 1. Hash Modulo and Bucket Indexing

A hash function maps arbitrary keys to integers; modulo by table size gives the direct bucket index.

```python
def bucket_index(key: str, num_buckets: int) -> int:
    return (hash(key) & 0x7FFFFFFF) % num_buckets

idx1 = bucket_index("apple", 8)
idx2 = bucket_index("banana", 8)
assert 0 <= idx1 < 8
assert 0 <= idx2 < 8
print(f"Bucket indices for 8 slots: 'apple' -> {idx1}, 'banana' -> {idx2}")
```

---

## 2. Linear Probing Collision Resolution

When a collision occurs at index `i`, linear probing sequentially checks `(i + 1) % size`, `(i + 2) % size`, until an empty slot is located.

```python
size = 5
table = [None] * size

def insert(key, val):
    idx = (hash(key) & 0x7FFFFFFF) % size
    while table[idx] is not None and table[idx][0] != key:
        idx = (idx + 1) % size
    table[idx] = (key, val)

insert("cat", 1)
insert("act", 2)  # possible collision with anagram
assert any(entry is not None for entry in table)
assert sum(1 for e in table if e is not None) == 2
print(f"Table after 2 inserts: {table}")
```

---

## 3. Frequency Counting with Hash Maps

Counting unique elements using a dictionary runs in $O(N)$ time with $O(U)$ space where $U$ is unique element count.

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

assert counts["apple"] == 3
assert counts["banana"] == 2
assert counts["cherry"] == 1
print(f"Frequency table: {counts}")
```

---
