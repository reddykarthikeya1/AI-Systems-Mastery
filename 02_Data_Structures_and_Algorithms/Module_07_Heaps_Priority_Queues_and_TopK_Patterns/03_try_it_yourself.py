"""Beginner playground for Module 07 - Heaps, Priority Queues & Top-K Patterns.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import heapq

# -------------------------------------------- 1. Min-Heap Array Invariant
h = [40, 10, 30, 20, 50]
heapq.heapify(h)
assert h[0] == 10, "Root must be the minimum element"
smallest = heapq.heappop(h)
assert smallest == 10
assert h[0] == 20, "Next smallest must rise to index 0"
print(f"Heapified array: {h}, extracted minimum: {smallest}")

# -------------------------------------------- 2. Streaming Top-K with a Bounded Min-Heap
stream = [5, 12, 3, 25, 1, 18, 9, 30, 2]
k = 3
k_heap = []
for num in stream:
    if len(k_heap) < k:
        heapq.heappush(k_heap, num)
    elif num > k_heap[0]:
        heapq.heapreplace(k_heap, num)

top_k = sorted(k_heap, reverse=True)
assert top_k == [30, 25, 18], "Top 3 numbers in stream"
assert len(k_heap) == 3
print(f"Top {k} numbers in stream: {top_k}")

# -------------------------------------------- 3. Max-Heap Emulation using Negation
max_h = []
for x in [10, 50, 20, 40]:
    heapq.heappush(max_h, -x)

largest = -heapq.heappop(max_h)
second_largest = -heapq.heappop(max_h)
assert largest == 50
assert second_largest == 40
print(f"Max-heap extracted in descending order: {largest}, {second_largest}")

print()
print("All checks passed.")
