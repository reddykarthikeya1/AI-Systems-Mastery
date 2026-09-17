"""Beginner playground for Module 01 - Python Fundamentals & Data Model.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import copy

# -------------------------------------------- 1. Reference Semantics and Object Identity
a = [1, 2, 3]
b = a
b.append(4)
assert a == [1, 2, 3, 4]
assert a is b
c = copy.deepcopy(a)
assert c == a
assert c is not a
print(f"Object identity verified: id(a)==id(b): {id(a)==id(b)}, id(a)==id(c): {id(a)==id(c)}")

# -------------------------------------------- 2. Comprehensions and Filtering
numbers = range(10)
evens_squared = [x**2 for x in numbers if x % 2 == 0]
assert evens_squared == [0, 4, 16, 36, 64]
assert len(evens_squared) == 5
print(f"Computed even squares: {evens_squared}")

# -------------------------------------------- 3. Dictionary Invariants and Keys
lookup = {(1, 2): "coordinate", "title": "metadata"}
assert lookup[(1, 2)] == "coordinate"
assert "title" in lookup
assert len(lookup) == 2
print("Hashable tuple key accessed successfully.")

print()
print("All checks passed.")
