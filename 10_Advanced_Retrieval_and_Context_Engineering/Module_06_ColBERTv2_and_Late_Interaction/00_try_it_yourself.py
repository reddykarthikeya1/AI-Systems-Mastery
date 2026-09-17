"""Beginner playground for Module 06 - ColBERTv2 & Late Interaction.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. ColBERT Token-Level MaxSim Scoring
# 2 query tokens, 3 document tokens (1D scalars for illustration)
E_q = [1.0, 0.5]
E_d = [0.2, 0.9, 0.4]

max_sim_q0 = max(E_q[0] * d for d in E_d)  # 1.0 * 0.9 = 0.9
max_sim_q1 = max(E_q[1] * d for d in E_d)  # 0.5 * 0.9 = 0.45
colbert_score = max_sim_q0 + max_sim_q1

assert max_sim_q0 == 0.9
assert max_sim_q1 == 0.45
assert colbert_score == 1.35
print(f"ColBERT MaxSim score: {colbert_score:.2f}")

# -------------------------------------------- 2. Late Interaction vs Single-Vector Bottleneck
doc_tokens = 128
emb_dim = 128
colbert_matrix_shape = (doc_tokens, emb_dim)
dense_vector_shape = (1, emb_dim)

assert colbert_matrix_shape[0] == 128
assert dense_vector_shape[0] == 1
print(f"ColBERT preserves {doc_tokens} distinct token vectors per passage.")

# -------------------------------------------- 3. Residual Vector Quantization Compression
raw_bytes = emb_dim * 2  # FP16 = 256 bytes
compressed_bytes = 20    # 20 bytes in ColBERTv2
compression_ratio = raw_bytes / compressed_bytes

assert compression_ratio > 10.0
assert round(compression_ratio, 1) == 12.8
print(f"ColBERTv2 achieves {compression_ratio:.1f}x compression on token vectors.")

print()
print("All checks passed.")
