"""Beginner playground for Module 10 - How to Fine-Tune Models & LoRA Math.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. LoRA Decomposition Factorization Delta W = B * A
d, k, r = 4096, 4096, 8
full_params = d * k
lora_params = (d * r) + (r * k)
param_reduction_pct = (1.0 - lora_params / full_params) * 100

assert full_params == 16_777_216
assert lora_params == 65_536
assert param_reduction_pct > 99.0
print(f"Parameter reduction: from {full_params:,} down to {lora_params:,} ({param_reduction_pct:.2f}% savings)")

# -------------------------------------------- 2. LoRA Scaling Factor Alpha / Rank
alpha = 16.0
rank = 8.0
scale = alpha / rank

assert scale == 2.0
assert scale > 0
print(f"LoRA adapter scale (alpha={alpha}, rank={rank}): {scale}")

# -------------------------------------------- 3. Frozen Base Weight Invariance
w0_weight = 1.42
lora_delta = 0.05 * scale
effective_weight = w0_weight + lora_delta

assert w0_weight == 1.42, "Base weight is frozen"
assert abs(effective_weight - 1.52) < 1e-6
print(f"Effective fine-tuned weight: {effective_weight:.4f}")

print()
print("All checks passed.")
