"""Beginner playground for Module 12 - Bonus Lessons: Quantization & Pruning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. FP32 to INT8 Symmetric Quantization
weights = [-2.5, 0.0, 1.25, 2.5]
max_abs = max(abs(w) for w in weights)
scale = max_abs / 127.0

int8_weights = [int(round(w / scale)) for w in weights]
assert int8_weights[0] == -127
assert int8_weights[1] == 0
assert int8_weights[-1] == 127
print(f"Quantized INT8 weights: {int8_weights} with scale {scale:.4f}")

# -------------------------------------------- 2. INT8 Dequantization Reconstruction
reconstructed = [q * scale for q in int8_weights]
for orig, recon in zip(weights, reconstructed):
    assert abs(orig - recon) < 0.02

assert abs(reconstructed[2] - 1.25) < 0.02
print(f"Dequantized weights match original: {reconstructed}")

# -------------------------------------------- 3. Magnitude-Based Weight Pruning
layer_w = [0.02, -0.85, 0.01, 0.45, -0.005]
threshold = 0.05
pruned = [0.0 if abs(w) < threshold else w for w in layer_w]

assert pruned == [0.0, -0.85, 0.0, 0.45, 0.0]
sparsity = pruned.count(0.0) / len(pruned)
assert sparsity == 0.60
print(f"Pruned layer: {pruned}, Sparsity: {sparsity:.1%}")

print()
print("All checks passed.")
