"""Beginner playground for Module 05 - Multi-Stage Retrieval & Reranking.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Bi-Encoder vs Cross-Encoder Architecture
q_len = 10
d_len = 90
bi_encoder_ops = q_len**2 + d_len**2      # 100 + 8100 = 8200
cross_encoder_ops = (q_len + d_len)**2     # 100^2 = 10,000

assert cross_encoder_ops > bi_encoder_ops
assert cross_encoder_ops == 10_000
print(f"Cross-encoder evaluates all cross-terms: {cross_encoder_ops} attention units.")

# -------------------------------------------- 2. Top-K Funnel Filtering
total_corpus = 1_000_000
stage1_retrieved = 100
stage2_reranked = 5

funnel_ratio = total_corpus / stage2_reranked
assert funnel_ratio == 200_000
assert stage1_retrieved > stage2_reranked
print(f"Retrieval funnel: {total_corpus:,} -> {stage1_retrieved} -> {stage2_reranked} context chunks.")

# -------------------------------------------- 3. Reranking Score Inversion
initial_ranks = ["doc_3", "doc_1", "doc_2"]
reranker_scores = {"doc_1": 0.95, "doc_2": 0.80, "doc_3": 0.20}
final_ranks = sorted(initial_ranks, key=lambda d: reranker_scores[d], reverse=True)

assert final_ranks == ["doc_1", "doc_2", "doc_3"]
assert final_ranks[0] != initial_ranks[0]
print(f"Reranker promoted {final_ranks[0]} to position #1 based on cross-attention score.")

print()
print("All checks passed.")
