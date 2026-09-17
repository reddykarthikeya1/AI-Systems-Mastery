"""Beginner playground for Module 02 - Contextual Retrieval Architecture.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# -------------------------------------------- 1. Contextual Header Prepending
doc_context = "Document: Apple Inc. Q3 2024 Earnings Report."
raw_chunk = "Services revenue grew 15% year-over-year reaching an all-time record."
contextual_chunk = f"{doc_context}\n{raw_chunk}"

assert "Apple Inc." in contextual_chunk
assert "Services revenue" in contextual_chunk
assert len(contextual_chunk) > len(raw_chunk)
print(f"Contextualized chunk:\n{contextual_chunk}")

# -------------------------------------------- 2. Embedding Drift Reduction
tags = ["finance", "earnings", "apple"]
assert "apple" in tags
print(f"Semantic metadata tags embedded: {tags}")

# -------------------------------------------- 3. Deduplication via Chunk Fingerprinting
h1 = hashlib.md5(raw_chunk.encode()).hexdigest()
h2 = hashlib.md5(raw_chunk.encode()).hexdigest()
assert h1 == h2
print(f"Deterministic chunk fingerprint: {h1[:8]}")

print()
print("All checks passed.")
