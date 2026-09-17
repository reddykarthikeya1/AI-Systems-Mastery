"""Beginner playground for Module 02 - Dynamic Arrays & Amortized Doubling.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import sys

# -------------------------------------------- 1. Geometric Growth and Total Element Copies
def simulate_growth(n):
    capacity = 1
    total_copies = 0
    for i in range(1, n + 1):
        if i > capacity:
            total_copies += (i - 1)
            capacity *= 2
    return total_copies, capacity

copies, cap = simulate_growth(1000)
assert cap == 1024, "Smallest power of 2 >= 1000"
assert copies < 2 * 1000, "Amortized doubling copies must be < 2N"
print(f"Appended 1000 items: final capacity={cap}, total copies={copies}")

# -------------------------------------------- 2. Two-Pointer In-Place Array Reversal
arr = [1, 2, 3, 4, 5]
left, right = 0, len(arr) - 1
while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1

assert arr == [5, 4, 3, 2, 1]
assert arr[0] == 5 and arr[-1] == 1
print(f"Reversed array in-place: {arr}")

# -------------------------------------------- 3. Prefix Sums for O(1) Range Queries
data = [2, 4, 6, 8, 10]
prefix = [0] * (len(data) + 1)
for i, x in enumerate(data):
    prefix[i + 1] = prefix[i] + x

def query(l, r):
    return prefix[r + 1] - prefix[l]

assert query(1, 3) == 18, "4 + 6 + 8 = 18"
assert query(0, 4) == 30, "Sum of all elements"
print(f"Prefix table: {prefix}, Query(1, 3) = {query(1, 3)}")

print()
print("All checks passed.")
