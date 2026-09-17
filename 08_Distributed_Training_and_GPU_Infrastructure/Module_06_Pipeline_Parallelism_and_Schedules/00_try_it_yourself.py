"""Beginner playground for Module 06 - Pipeline Parallelism & 1F1B Schedule.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Pipeline Bubble Ratio Math
p = 4   # 4 pipeline stages
m = 16  # 16 micro-batches
bubble_ratio = (p - 1) / (m + p - 1)

assert abs(bubble_ratio - 3 / 19) < 1e-4
assert bubble_ratio < 0.20
print(f"Pipeline bubble ratio with p={p}, m={m}: {bubble_ratio:.1%}")

# -------------------------------------------- 2. One-Forward-One-Backward (1F1B) Schedule
max_active_activations = p  # Stays bounded by number of pipeline stages
assert max_active_activations == 4
print(f"1F1B keeps peak in-flight activations bounded to {max_active_activations} micro-batches.")

# -------------------------------------------- 3. Activation Checkpointing Tradeoff
mem_without_checkpoints = 10.0  # GB
mem_with_checkpoints = 3.0     # GB
compute_overhead_pct = 33.0

assert mem_with_checkpoints < mem_without_checkpoints
assert mem_with_checkpoints / mem_without_checkpoints == 0.3
print(f"Activation checkpointing memory: {mem_with_checkpoints} GB vs {mem_without_checkpoints} GB baseline.")

print()
print("All checks passed.")
