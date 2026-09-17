"""Beginner playground for Module 10 - Scaling Laws, Profiling & FinOps.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Chinchilla Optimal Token-to-Parameter Ratio (20x)
params = 7_000_000_000  # 7B model
optimal_tokens = 20 * params

assert optimal_tokens == 140_000_000_000  # 140 Billion tokens
assert optimal_tokens / params == 20
print(f"Chinchilla optimal token count for 7B model: {optimal_tokens / 1e9:.0f} Billion tokens.")

# -------------------------------------------- 2. Total Training FLOPs Estimation C = 6 * N * D
N = 7e9
D = 140e9
total_flops = 6 * N * D

assert total_flops == 5.88e21
print(f"Total training FLOPs: {total_flops:.2e}")

# -------------------------------------------- 3. Training Cost & GPU Hours Estimation
h100_sxm_tflops = 312e12
mfu = 0.40
effective_tflops = h100_sxm_tflops * mfu
gpu_seconds = total_flops / effective_tflops
gpu_hours = gpu_seconds / 3600
cost_at_3_per_hr = gpu_hours * 3.0

assert gpu_hours > 0
print(f"Estimated GPU hours: {gpu_hours:,.0f} hrs (~${cost_at_3_per_hr:,.2f})")

print()
print("All checks passed.")
