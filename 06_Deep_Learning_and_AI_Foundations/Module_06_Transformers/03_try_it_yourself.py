"""Beginner playground for Module 06 - Transformers & Self-Attention.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Scaled Dot-Product Attention Scores
q = [1.0, 0.0]
k1 = [1.0, 0.0]  # Identical direction
k2 = [0.0, 1.0]  # Orthogonal direction
d_k = 2.0
scale = math.sqrt(d_k)

score1 = sum(a * b for a, b in zip(q, k1)) / scale
score2 = sum(a * b for a, b in zip(q, k2)) / scale

assert score1 > score2
assert abs(score1 - 1.0 / math.sqrt(2.0)) < 1e-6
assert score2 == 0.0
print(f"Attention scores: match={score1:.4f}, orthogonal={score2:.4f}")

# -------------------------------------------- 2. Attention Weights via Softmax
scores = [score1, score2]
exp_s = [math.exp(s) for s in scores]
weights = [e / sum(exp_s) for e in exp_s]

assert abs(sum(weights) - 1.0) < 1e-6
assert weights[0] > weights[1]
print(f"Attention weights distribution: {[round(w, 4) for w in weights]}")

# -------------------------------------------- 3. Weighted Value Context Aggregation
v1 = [10.0, 20.0]
v2 = [1.0, 2.0]

context = [weights[0] * v1[i] + weights[1] * v2[i] for i in range(2)]
assert len(context) == 2
assert context[0] > 1.0
print(f"Aggregated context embedding: {[round(c, 2) for c in context]}")

print()
print("All checks passed.")
