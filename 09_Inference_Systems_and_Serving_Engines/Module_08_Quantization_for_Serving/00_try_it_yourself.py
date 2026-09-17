"""Beginner playground for Module 08 - Quantization for Serving (AWQ & SmoothQuant).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Activation Outlier Channel Dilemma
channel_act = [0.2, 0.1, 85.0, 0.3]
max_outlier = max(channel_act)
median_act = sorted(channel_act)[1]
ratio = max_outlier / median_act

assert ratio > 100.0
assert ratio == 425.0
print(f"Activation outlier channel ratio: {ratio:.0f}x baseline magnitude.")

# -------------------------------------------- 2. SmoothQuant Mathematical Equivalence
x = 10.0
w = 0.2
s = 2.0

x_smooth = x / s   # 5.0
w_smooth = w * s   # 0.4

assert x * w == 2.0
assert x_smooth * w_smooth == 2.0
print(f"SmoothQuant identity verified: {x}*{w} == {x_smooth}*{w_smooth}")

# -------------------------------------------- 3. Weight-Only (W4A16) Memory Footprint Halving
fp16_gb = 14.0
int4_gb = fp16_gb * (4 / 16)

assert int4_gb == 3.5
assert fp16_gb / int4_gb == 4.0
print(f"W4A16 shrinks model from {fp16_gb} GB down to {int4_gb} GB.")

print()
print("All checks passed.")
