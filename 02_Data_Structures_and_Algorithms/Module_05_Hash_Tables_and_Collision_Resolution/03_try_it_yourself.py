"""Beginner playground for Module 05 - Hash Tables & Collision Resolution.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# -------------------------------------------- 1. Hash Modulo and Bucket Indexing
def bucket_index(key: str, num_buckets: int) -> int:
    return (hash(key) & 0x7FFFFFFF) % num_buckets

idx1 = bucket_index("apple", 8)
idx2 = bucket_index("banana", 8)
assert 0 <= idx1 < 8
assert 0 <= idx2 < 8
print(f"Bucket indices for 8 slots: 'apple' -> {idx1}, 'banana' -> {idx2}")

# -------------------------------------------- 2. Linear Probing Collision Resolution
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

# -------------------------------------------- 3. Frequency Counting with Hash Maps
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

assert counts["apple"] == 3
assert counts["banana"] == 2
assert counts["cherry"] == 1
print(f"Frequency table: {counts}")

print()
print("All checks passed.")
