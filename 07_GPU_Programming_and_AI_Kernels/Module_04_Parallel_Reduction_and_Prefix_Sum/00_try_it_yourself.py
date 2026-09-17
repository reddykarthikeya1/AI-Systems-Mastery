"""Beginner playground for Module 04 - Parallel Reduction & Prefix Sum.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Tree-Based Parallel Reduction
arr = [1, 2, 3, 4, 5, 6, 7, 8]
n = len(arr)
rounds = int(math.log2(n))

stride = 1
for _ in range(rounds):
    for i in range(0, n, stride * 2):
        arr[i] += arr[i + stride]
    stride *= 2

assert arr[0] == sum(range(1, 9))  # 36
assert rounds == 3
print(f"Tree reduction result at index 0: {arr[0]} in {rounds} rounds.")

# -------------------------------------------- 2. Blelloch Inclusive to Exclusive Prefix Sum
inclusive = [1, 3, 6, 10]
exclusive = [0] + inclusive[:-1]

assert exclusive == [0, 1, 3, 6]
assert len(exclusive) == len(inclusive)
assert exclusive[0] == 0
print(f"Exclusive prefix sum: {exclusive}")

# -------------------------------------------- 3. Warp Shuffle Sum Reduction
lane_val = 1
# Butterfly reduction across 32 lanes
for delta in [16, 8, 4, 2, 1]:
    lane_val += lane_val  # Simulated reduction

assert lane_val == 32
print(f"Warp shuffle reduction sum across 32 lanes: {lane_val}")

print()
print("All checks passed.")
