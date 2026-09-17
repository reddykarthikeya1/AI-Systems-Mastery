"""Beginner playground for Module 09 - FlashAttention-3 & Hopper/Blackwell.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Tensor Memory Accelerator (TMA) Asynchronous Copy
tile_shape = (64, 64)
bytes_per_elem = 2
tile_bytes = tile_shape[0] * tile_shape[1] * bytes_per_elem

assert tile_bytes == 8192
assert tile_bytes == 8 * 1024
print(f"TMA copied 8 KB tile ({tile_shape}) asynchronously into shared memory.")

# -------------------------------------------- 2. FP8 Low-Precision Dynamic Range Scaling
fp16_bits = 16
fp8_bits = 8
bandwidth_multiplier = fp16_bits / fp8_bits

assert bandwidth_multiplier == 2.0
print(f"FP8 doubles memory bandwidth efficiency by {bandwidth_multiplier:.0f}x.")

# -------------------------------------------- 3. Warp-Group Matrix Multiply-Accumulate (WGMMA)
threads_per_warpgroup = 4 * 32
assert threads_per_warpgroup == 128
print(f"WGMMA synchronizes {threads_per_warpgroup} threads as a single warp-group.")

print()
print("All checks passed.")
