"""Beginner playground for Module 01 - GPU Microarchitecture and Execution Model.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Warp Execution Dimension (32 Threads)
threads_per_warp = 32
total_threads = 1024
num_warps = total_threads // threads_per_warp

assert num_warps == 32
assert total_threads % threads_per_warp == 0
print(f"Total threads: {total_threads} partitioned into {num_warps} SIMT warps.")

# -------------------------------------------- 2. Global Linear Thread Indexing
def get_global_tid(block_idx, thread_idx, block_dim):
    return block_idx * block_dim + thread_idx

tid_0_0 = get_global_tid(0, 0, 256)
tid_1_5 = get_global_tid(1, 5, 256)
assert tid_0_0 == 0
assert tid_1_5 == 261
assert get_global_tid(3, 255, 256) == 1023
print(f"Global thread IDs: block 0 thread 0 -> {tid_0_0}, block 1 thread 5 -> {tid_1_5}")

# -------------------------------------------- 3. Grid Boundary Guard (Bounds Check)
N = 1000
block_dim = 256
grid_dim = math.ceil(N / block_dim)  # 4 blocks -> 1024 threads

active_count = 0
for b in range(grid_dim):
    for t in range(block_dim):
        tid = b * block_dim + t
        if tid < N:
            active_count += 1

assert grid_dim == 4
assert active_count == 1000
assert (grid_dim * block_dim) == 1024
print(f"Boundary check passed: exactly {active_count} of {grid_dim * block_dim} threads activated.")

print()
print("All checks passed.")
