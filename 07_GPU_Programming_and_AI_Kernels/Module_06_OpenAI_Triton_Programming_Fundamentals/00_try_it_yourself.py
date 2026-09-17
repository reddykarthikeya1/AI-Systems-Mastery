"""Beginner playground for Module 06 - OpenAI Triton Fundamentals.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Block Pointer Offsets and Range Masks
block_size = 64
pid = 2
offsets = [pid * block_size + i for i in range(block_size)]
n_elements = 150
mask = [off < n_elements for off in offsets]

assert offsets[0] == 128
assert offsets[-1] == 191
assert sum(mask) == 22, "150 - 128 = 22 elements inside bounds"
print(f"Triton block offsets {offsets[0]}..{offsets[-1]}, valid masked elements: {sum(mask)}")

# -------------------------------------------- 2. Triton Vectorized Add Kernel Simulation
x = list(range(10))
y = [x_val * 2 for x_val in x]
output = [0] * len(x)

for i in range(len(x)):
    output[i] = x[i] + y[i]

assert output == [3 * i for i in range(10)]
assert output[-1] == 27
print(f"Triton simulated vector add result: {output}")

# -------------------------------------------- 3. Triton Autotuning Grid Search
configs = [(32, 2), (64, 4), (128, 8)]
best_config = max(configs, key=lambda c: c[0] * c[1])

assert best_config == (128, 8)
assert best_config[0] == 128
print(f"Selected best autotuned configuration: BLOCK_SIZE={best_config[0]}, WARPS={best_config[1]}")

print()
print("All checks passed.")
