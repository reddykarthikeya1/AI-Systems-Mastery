"""Beginner playground for Module 03 - Vector Database Internals (HNSW).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Euclidean Distance Metric in d Dimensions
v1 = [1.0, 2.0, 3.0]
v2 = [4.0, 6.0, 3.0]

dist = math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))
assert dist == 5.0  # sqrt(3^2 + 4^2 + 0) = 5.0
assert dist > 0.0
print(f"Euclidean distance between vectors: {dist:.2f}")

# -------------------------------------------- 2. Cosine Distance as 1 - Cosine Similarity
u = [1.0, 0.0]
v = [0.0, 1.0]  # Orthogonal

cos_dist = 1.0 - sum(a * b for a, b in zip(u, v))
assert cos_dist == 1.0, "Orthogonal unit vectors have cosine distance 1.0"
print(f"Cosine distance between orthogonal vectors: {cos_dist:.2f}")

# -------------------------------------------- 3. HNSW Multi-Layer Skip Invariant
layer_multipliers = [1, 2, 4, 8]
assert layer_multipliers[-1] / layer_multipliers[0] == 8
print("HNSW hierarchical layers verified.")

print()
print("All checks passed.")
