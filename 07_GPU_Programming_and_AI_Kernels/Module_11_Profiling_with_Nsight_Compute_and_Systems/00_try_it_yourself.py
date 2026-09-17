"""Beginner playground for Module 11 - Profiling with Nsight Compute & Roofline.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Roofline Ridge Point Calculation
peak_tflops = 312.0   # Tensor core dense FP16 TFLOP/s
peak_bw_tbs = 2.0     # HBM bandwidth in TB/s
ridge_intensity = peak_tflops / peak_bw_tbs  # FLOP/byte

assert ridge_intensity == 156.0
print(f"Hardware Ridge Point: {ridge_intensity:.1f} FLOP/byte.")

# -------------------------------------------- 2. Kernel Regime Classification
kernel1_intensity = 40.0   # Softmax / LayerNorm
kernel2_intensity = 200.0  # Large GEMM

regime1 = "Memory Bound" if kernel1_intensity < ridge_intensity else "Compute Bound"
regime2 = "Memory Bound" if kernel2_intensity < ridge_intensity else "Compute Bound"

assert regime1 == "Memory Bound"
assert regime2 == "Compute Bound"
print(f"Kernel 1: {regime1}, Kernel 2: {regime2}")

# -------------------------------------------- 3. Memory Bandwidth Utilization (MBU)
achieved_gb_s = 1700.0
peak_gb_s = 2000.0
mbu_pct = (achieved_gb_s / peak_gb_s) * 100.0

assert mbu_pct == 85.0
assert mbu_pct > 80.0, "High memory bus saturation achieved"
print(f"Achieved Memory Bandwidth Utilization: {mbu_pct:.1f}%")

print()
print("All checks passed.")
