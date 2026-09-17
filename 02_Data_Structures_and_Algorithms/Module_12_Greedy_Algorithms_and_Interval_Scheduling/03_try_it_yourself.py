"""Beginner playground for Module 12 - Greedy Algorithms & Interval Scheduling.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Earliest Finish Time Interval Scheduling
intervals = [(1, 4), (2, 3), (3, 5), (0, 6), (5, 7), (6, 9)]
intervals.sort(key=lambda x: x[1])

selected = []
last_end = float('-inf')
for start, end in intervals:
    if start >= last_end:
        selected.append((start, end))
        last_end = end

assert len(selected) == 3
assert selected == [(2, 3), (3, 5), (5, 7)]
print(f"Max non-overlapping intervals: {selected}")

# -------------------------------------------- 2. Jump Game Maximum Reach Frontier
def can_jump(nums):
    farthest = 0
    for i, x in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + x)
        if farthest >= len(nums) - 1:
            return True
    return farthest >= len(nums) - 1

assert can_jump([2, 3, 1, 1, 4]) is True
assert can_jump([3, 2, 1, 0, 4]) is False
assert can_jump([0]) is True
print("Jump game reachability verified.")

# -------------------------------------------- 3. Greedy Coin Change for Canonical Systems
def greedy_change(amount, coins=[25, 10, 5, 1]):
    used = {}
    for c in coins:
        count = amount // c
        if count > 0:
            used[c] = count
            amount %= c
    return used

change = greedy_change(41)
assert change == {25: 1, 10: 1, 5: 1, 1: 1}
assert sum(k * v for k, v in change.items()) == 41
print(f"Greedy change for 41 cents: {change}")

print()
print("All checks passed.")
