"""Beginner playground for Module 08 - Linear Algebra in Models.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Dense Layer Affine Map y = W*x + b
W = [[0.5, -0.2],
     [0.8,  0.4]]
b = [0.1, -0.05]
x = [1.0, 2.0]

y = [sum(W[r][c] * x[c] for c in range(2)) + b[r] for r in range(2)]
assert abs(y[0] - (0.5 * 1.0 - 0.2 * 2.0 + 0.1)) < 1e-6
assert abs(y[0] - 0.2) < 1e-6
assert abs(y[1] - 1.55) < 1e-6
print(f"Affine transformation output: y={y}")

# -------------------------------------------- 2. Cosine Similarity for Embedding Comparison
emb1 = [1.0, 2.0, 0.0]
emb2 = [2.0, 4.0, 0.0]  # Parallel direction

dot = sum(a * b for a, b in zip(emb1, emb2))
norm1 = math.sqrt(sum(a**2 for a in emb1))
norm2 = math.sqrt(sum(a**2 for a in emb2))
cos_sim = dot / (norm1 * norm2)

assert abs(cos_sim - 1.0) < 1e-6, "Parallel vectors have cosine similarity 1.0"
print(f"Cosine similarity between parallel embeddings: {cos_sim:.4f}")

# -------------------------------------------- 3. Softmax Normalization Invariant
logits = [2.0, 1.0, 0.1]
exp_vals = [math.exp(z) for z in logits]
sum_exp = sum(exp_vals)
probs = [ev / sum_exp for ev in exp_vals]

assert abs(sum(probs) - 1.0) < 1e-6, "Probabilities must sum to 1.0"
assert all(p >= 0.0 for p in probs)
assert probs[0] > probs[1] > probs[2]
print(f"Logits {logits} -> Softmax probabilities: {[round(p, 4) for p in probs]}")

print()
print("All checks passed.")
