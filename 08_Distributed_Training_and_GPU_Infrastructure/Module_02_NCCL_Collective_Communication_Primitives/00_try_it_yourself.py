"""Beginner playground for Module 02 - NCCL Collective Communication Primitives.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. AllReduce via ReduceScatter + AllGather
data_per_gpu = [1.0, 2.0, 3.0]  # GPU 0
num_gpus = 4
total_data_size = 100  # MB
volume_transferred = 2 * ((num_gpus - 1) / num_gpus) * total_data_size

assert volume_transferred == 2 * (3 / 4) * 100  # 150 MB
assert volume_transferred < 2 * total_data_size
print(f"Total data sent per GPU in 4-GPU Ring-AllReduce: {volume_transferred} MB")

# -------------------------------------------- 2. Broadcast Primitive Invariant
ranks = [0, 1, 2, 3]
root_val = 42
cluster_state = [root_val if r == 0 else 0 for r in ranks]

# Broadcast from rank 0
for r in range(len(cluster_state)):
    cluster_state[r] = cluster_state[0]

assert all(val == 42 for val in cluster_state)
assert len(cluster_state) == 4
print(f"Broadcast replicated value 42 across all ranks: {cluster_state}")

# -------------------------------------------- 3. Reduce-Scatter Chunk Partitioning
gpu_tensors = [[1, 10], [2, 20], [3, 30]]  # 3 GPUs, 2 elements each
chunk_0_sum = sum(t[0] for t in gpu_tensors)
chunk_1_sum = sum(t[1] for t in gpu_tensors)

assert chunk_0_sum == 6
assert chunk_1_sum == 60
print(f"Reduce-Scatter outputs: chunk 0 -> {chunk_0_sum}, chunk 1 -> {chunk_1_sum}")

print()
print("All checks passed.")
