"""Beginner playground for Module 08 - 3D Parallelism Integration & Orchestration.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Cluster Grid 3D Dimensions
TP, PP, DP = 4, 8, 16
total_gpus = TP * PP * DP

assert total_gpus == 512
assert total_gpus % (TP * PP) == 0
print(f"3D Parallel grid: TP={TP}, PP={PP}, DP={DP} utilizes {total_gpus} GPUs.")

# -------------------------------------------- 2. Rank Mapping to 3D Coordinates
def get_3d_coords(rank, tp, pp, dp):
    tp_id = rank % tp
    pp_id = (rank // tp) % pp
    dp_id = rank // (tp * pp)
    return tp_id, pp_id, dp_id

coords = get_3d_coords(100, 4, 8, 16)
assert coords == (0, 1, 3)
assert get_3d_coords(0, 4, 8, 16) == (0, 0, 0)
print(f"Rank 100 mapped to 3D grid: TP={coords[0]}, PP={coords[1]}, DP={coords[2]}")

# -------------------------------------------- 3. Total Training Throughput Calculation
mfu = 0.45  # Model FLOPs Utilization 45%
tflops_per_gpu = 300.0
effective_pflops = (total_gpus * tflops_per_gpu * mfu) / 1000.0

assert round(effective_pflops, 2) == 69.12
print(f"Effective cluster compute throughput: {effective_pflops:.2f} PFLOP/s")

print()
print("All checks passed.")
