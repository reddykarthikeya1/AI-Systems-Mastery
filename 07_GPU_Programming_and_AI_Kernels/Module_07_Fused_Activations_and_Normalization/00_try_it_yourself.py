"""Beginner playground for Module 07 - Fused Activations & Normalization.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Unfused vs Fused Memory Trips
unfused_dram_passes = 4  # (read x, write norm) + (read norm, write relu)
fused_dram_passes = 2    # read x, write final
speedup = unfused_dram_passes / fused_dram_passes

assert speedup == 2.0
assert fused_dram_passes < unfused_dram_passes
print(f"Kernel fusion eliminates {unfused_dram_passes - fused_dram_passes} DRAM round trips ({speedup}x speedup).")

# -------------------------------------------- 2. Layer Normalization Statistics
x = [1.0, 2.0, 3.0, 4.0, 5.0]
mean = sum(x) / len(x)
var = sum((val - mean)**2 for val in x) / len(x)
normed = [(val - mean) / math.sqrt(var + 1e-5) for val in x]

assert abs(mean - 3.0) < 1e-6
assert abs(sum(normed)) < 1e-4, "Normalized mean is 0"
assert abs(sum(v**2 for v in normed) / len(normed) - 1.0) < 1e-3, "Normalized variance is 1"
print(f"Normalized activations: {[round(v, 3) for v in normed]}")

# -------------------------------------------- 3. Fused Bias-GELU Activation
def gelu(z):
    return 0.5 * z * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (z + 0.044715 * z**3)))

val_fused = gelu(1.5 + 0.5)  # Bias + GELU in single expression
assert val_fused > 1.9
assert gelu(0.0) == 0.0
print(f"Fused Bias-GELU output: {val_fused:.4f}")

print()
print("All checks passed.")
