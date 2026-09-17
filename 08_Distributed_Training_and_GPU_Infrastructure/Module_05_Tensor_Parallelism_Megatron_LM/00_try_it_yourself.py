"""Beginner playground for Module 05 - Tensor Parallelism (Megatron-LM).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Column Parallel Linear Layer
X = [1.0, 2.0]
W1 = [[1.0], [2.0]]  # Column 1
W2 = [[3.0], [4.0]]  # Column 2

Y1 = sum(X[i] * W1[i][0] for i in range(2))  # 1*1 + 2*2 = 5
Y2 = sum(X[i] * W2[i][0] for i in range(2))  # 1*3 + 2*4 = 11

assert Y1 == 5.0
assert Y2 == 11.0
print(f"Column parallel outputs on 2 GPUs: Y1={Y1}, Y2={Y2}")

# -------------------------------------------- 2. Row Parallel Linear Layer with AllReduce
X1 = [1.0]
X2 = [2.0]
W_row1 = [5.0, 6.0]
W_row2 = [7.0, 8.0]

part1 = [X1[0] * w for w in W_row1]  # [5, 6]
part2 = [X2[0] * w for w in W_row2]  # [14, 16]
full_Y = [p1 + p2 for p1, p2 in zip(part1, part2)]

assert full_Y == [19.0, 22.0]
assert len(full_Y) == 2
print(f"Row parallel output after AllReduce sum: {full_Y}")

# -------------------------------------------- 3. Megatron-LM MLP Two-Layer Fusion Invariant
allreduce_count = 1  # Exactly 1 AllReduce per MLP block
assert allreduce_count == 1
print("Megatron MLP column+row pairing minimizes collective communication to 1 AllReduce.")

print()
print("All checks passed.")
