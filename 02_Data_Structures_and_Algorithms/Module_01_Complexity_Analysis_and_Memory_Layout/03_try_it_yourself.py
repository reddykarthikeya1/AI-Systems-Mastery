"""Beginner playground for Module 01 - Complexity Analysis & Bit Manipulation.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Bitwise Parity and Power of Two Invariant
val = 16
is_even = (val & 1) == 0
assert is_even is True, "16 must be even"

is_power_of_two = (val > 0) and ((val & (val - 1)) == 0)
assert is_power_of_two is True, "16 is 2^4"
assert ((15 & 14) == 0) is False, "15 is not a power of two"
print(f"val={val}: is_even={is_even}, is_power_of_two={is_power_of_two}")

# -------------------------------------------- 2. Fast Multiplication and Division via Bit Shifts
base = 7
doubled = base << 1
halved = base >> 1
assert doubled == 14
assert halved == 3
assert (1 << 10) == 1024, "2^10 must equal 1024"
print(f"base={base}: doubled={doubled}, halved={halved}, 2^10={1 << 10}")

# -------------------------------------------- 3. The Self-Cancelling XOR Invariant
nums = [4, 1, 2, 1, 2]
unique = 0
for x in nums:
    unique ^= x

assert unique == 4, "4 is the only unpaired number"
assert (99 ^ 99) == 0
assert (0 ^ 42) == 42
print(f"Array {nums} isolated unique element: {unique}")

print()
print("All checks passed.")
