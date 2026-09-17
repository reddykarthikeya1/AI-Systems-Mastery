"""Beginner playground for Module 04 - Hybrid Search & Reciprocal Rank Fusion.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import defaultdict

# -------------------------------------------- 1. Reciprocal Rank Fusion (RRF) Formula
k = 60
# Rank lists (1-indexed)
dense_ranks = {"doc_1": 1, "doc_2": 2, "doc_3": 3}
sparse_ranks = {"doc_2": 1, "doc_1": 3, "doc_4": 2}

rrf_scores = defaultdict(float)
for doc, r in dense_ranks.items():
    rrf_scores[doc] += 1.0 / (k + r)
for doc, r in sparse_ranks.items():
    rrf_scores[doc] += 1.0 / (k + r)

# doc_2: rank 2 dense (1/62) + rank 1 sparse (1/61)
score_doc2 = 1/62 + 1/61
assert abs(rrf_scores["doc_2"] - score_doc2) < 1e-6
best_doc = max(rrf_scores, key=rrf_scores.get)
assert best_doc == "doc_2"
print(f"RRF ranked '{best_doc}' #1 with score {rrf_scores[best_doc]:.5f}")

# -------------------------------------------- 2. BM25 Term Frequency Saturation
k1 = 1.2
def bm25_tf_weight(tf):
    return (tf * (k1 + 1)) / (tf + k1)

w_1 = bm25_tf_weight(1)
w_10 = bm25_tf_weight(10)
w_100 = bm25_tf_weight(100)

assert w_1 < w_10 < w_100
assert w_100 < k1 + 1  # Bounded by k1 + 1 = 2.2
print(f"BM25 TF weights: tf=1 -> {w_1:.2f}, tf=10 -> {w_10:.2f}, tf=100 -> {w_100:.2f}")

# -------------------------------------------- 3. Complementary Precision Analysis
results_count = len(rrf_scores)
assert results_count == 4
print(f"Fused candidate pool contains {results_count} distinct documents.")

print()
print("All checks passed.")
