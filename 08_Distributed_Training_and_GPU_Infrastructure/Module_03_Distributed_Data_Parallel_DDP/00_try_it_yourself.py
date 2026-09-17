"""Beginner playground for Module 03 - Distributed Data Parallel (DDP).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Gradient Averaging Across Ranks
grad_gpu0 = [0.2, 0.4]
grad_gpu1 = [0.4, 0.8]
world_size = 2

avg_grad = [(g0 + g1) / world_size for g0, g1 in zip(grad_gpu0, grad_gpu1)]
assert abs(avg_grad[0] - 0.3) < 1e-6 and abs(avg_grad[1] - 0.6) < 1e-6
assert len(avg_grad) == 2
print(f"Synchronized average gradients: {avg_grad}")

# -------------------------------------------- 2. Gradient Bucketing to Overlap Compute and Comm
bucket_size_mb = 25.0
param_grads = [5.0, 12.0, 10.0, 8.0]  # Sizes in MB
buckets = []
current_bucket = 0.0

for g in param_grads:
    if current_bucket + g > bucket_size_mb:
        buckets.append(current_bucket)
        current_bucket = g
    else:
        current_bucket += g
buckets.append(current_bucket)

assert len(buckets) == 2
assert buckets[0] == 17.0  # 5 + 12
assert buckets[1] == 18.0  # 10 + 8
print(f"Buckets formed: {buckets} MB (threshold: {bucket_size_mb} MB)")

# -------------------------------------------- 3. Effective Global Batch Size Scaling
per_device_batch = 4
world_size = 8
grad_accum = 4
global_batch = per_device_batch * world_size * grad_accum

assert global_batch == 128
print(f"Global effective batch size: {global_batch}")

print()
print("All checks passed.")
