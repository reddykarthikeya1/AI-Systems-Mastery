"""Beginner playground for Module 08 - Query Transformation & Agentic RAG.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Query Decomposition into Sub-Queries
complex_query = "Compare revenue growth of Apple and Microsoft in 2024."
sub_queries = [
    "What was Apple's revenue growth in 2024?",
    "What was Microsoft's revenue growth in 2024?"
]

assert len(sub_queries) == 2
assert "Apple" in sub_queries[0]
assert "Microsoft" in sub_queries[1]
print(f"Decomposed '{complex_query}' into {len(sub_queries)} sub-queries.")

# -------------------------------------------- 2. Hypothetical Document Embeddings (HyDE)
raw_q = "How do transformers prevent quadratic attention memory?"
hypothetical_answer = "Transformers use FlashAttention or tiling to compute softmax in SRAM blocks without materializing N x N matrices."

assert "FlashAttention" in hypothetical_answer
assert len(hypothetical_answer) > len(raw_q)
print("HyDE generated document-like target embedding.")

# -------------------------------------------- 3. Self-Correction & Fallback Trigger
retrieval_confidence = 0.32
threshold = 0.70
trigger_fallback = retrieval_confidence < threshold

assert trigger_fallback is True
print("Retrieval confidence low: query reformulator triggered.")

print()
print("All checks passed.")
