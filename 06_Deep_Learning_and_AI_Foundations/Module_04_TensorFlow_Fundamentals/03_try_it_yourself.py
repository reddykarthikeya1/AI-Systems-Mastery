"""Beginner playground for Module 04 - TensorFlow Fundamentals & Static Graphs.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Tensor Shape and Stride Manipulation
shape = (2, 3)
total_elements = shape[0] * shape[1]
strides = (shape[1], 1)

assert total_elements == 6
assert strides == (3, 1)
print(f"Tensor shape {shape} has {total_elements} elements with strides {strides}")

# -------------------------------------------- 2. Flattening and Index Coordinate Mapping
def to_1d(r, c, cols):
    return r * cols + c

assert to_1d(0, 0, 3) == 0
assert to_1d(1, 2, 3) == 5
assert to_1d(1, 0, 3) == 3
print("Row-major coordinate translation verified.")

# -------------------------------------------- 3. Broadcasting Semantics
matrix = [[1, 2, 3], [4, 5, 6]]
bias_vec = [10, 20, 30]

result = [[matrix[r][c] + bias_vec[c] for c in range(3)] for r in range(2)]
assert result[0] == [11, 22, 33]
assert result[1] == [14, 25, 36]
print(f"Broadcasted addition result: {result}")

print()
print("All checks passed.")
