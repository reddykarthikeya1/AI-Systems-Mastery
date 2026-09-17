"""Beginner playground for Module 02 - CUDA C++ Programming Fundamentals.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Vector Addition Kernel Simulation
A = [1.0, 2.0, 3.0, 4.0]
B = [10.0, 20.0, 30.0, 40.0]
C = [0.0] * len(A)

# Simulated parallel thread loop
for tid in range(len(A)):
    C[tid] = A[tid] + B[tid]

assert C == [11.0, 22.0, 33.0, 44.0]
assert C[0] == 11.0
print(f"Parallel vector add result: {C}")

# -------------------------------------------- 2. Grid Stride Loop Pattern
total_threads = 4
data_size = 10
processed = [0] * data_size

for tid in range(total_threads):
    # Each thread steps forward by total_threads
    for i in range(tid, data_size, total_threads):
        processed[i] = 1

assert sum(processed) == data_size
assert all(p == 1 for p in processed)
print(f"Grid-stride loop processed all {data_size} elements with {total_threads} threads.")

# -------------------------------------------- 3. Speedup over Sequential Baseline
seq_ops = 1_000_000
gpu_cores = 1000
parallel_time_units = seq_ops / gpu_cores

assert parallel_time_units == 1000.0
assert seq_ops / parallel_time_units == 1000.0
print(f"Theoretical speedup with {gpu_cores} cores: {gpu_cores}x")

print()
print("All checks passed.")
