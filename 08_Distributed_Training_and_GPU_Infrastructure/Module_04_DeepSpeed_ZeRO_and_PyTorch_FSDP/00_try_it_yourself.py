"""Beginner playground for Module 04 - DeepSpeed ZeRO & PyTorch FSDP.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Adam Optimizer State Memory Footprint (16 Bytes / Param)
num_params = 1_000_000_000  # 1 Billion params
bytes_per_param_adam = 16
total_gb = (num_params * bytes_per_param_adam) / (1024**3)

assert round(total_gb, 1) == 14.9
assert bytes_per_param_adam == 16
print(f"Adam training state memory for 1B model: {total_gb:.2f} GB")

# -------------------------------------------- 2. ZeRO-1 Optimizer State Sharding
world_size = 8
sharded_adam_gb = (num_params * 12) / (world_size * (1024**3))  # 12 bytes of Adam states sharded

assert sharded_adam_gb < total_gb
assert round(sharded_adam_gb, 2) == 1.40
print(f"ZeRO-1 sharded optimizer memory on 8 GPUs: {sharded_adam_gb:.2f} GB per GPU.")

# -------------------------------------------- 3. ZeRO-3 Full Sharding Memory Savings
zero3_memory_per_gpu = total_gb / world_size
assert round(zero3_memory_per_gpu, 2) == 1.86
print(f"ZeRO-3 memory per GPU on 8 GPUs: {zero3_memory_per_gpu:.2f} GB (8x reduction)")

print()
print("All checks passed.")
