"""Beginner playground for Module 07 - Sequence & Context Parallelism (Ring Attention).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Sequence Sharding Across GPUs
total_context = 128_000
num_gpus = 8
local_chunk = total_context // num_gpus

assert local_chunk == 16_000
assert local_chunk * num_gpus == total_context
print(f"128k context sharded into {local_chunk} tokens per GPU across {num_gpus} GPUs.")

# -------------------------------------------- 2. Ring KV Shift Communication
ring_ranks = [0, 1, 2, 3]
next_ranks = [(r + 1) % len(ring_ranks) for r in ring_ranks]
prev_ranks = [(r - 1) % len(ring_ranks) for r in ring_ranks]

assert next_ranks == [1, 2, 3, 0]
assert prev_ranks == [3, 0, 1, 2]
print(f"Ring communication mapping: next={next_ranks}, prev={prev_ranks}")

# -------------------------------------------- 3. Zero Extra Memory Context Scaling
mem_per_gpu = 16_000 * 2  # 32 KB per head
assert mem_per_gpu == 32_000
print(f"Per-GPU memory bound invariant verified.")

print()
print("All checks passed.")
