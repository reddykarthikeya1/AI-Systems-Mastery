"""Beginner playground for Module 01 - Parsing & Hierarchical Chunking.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Fixed-Size Chunking with Overlap
text = "abcdefghijklmnopqrstuvwxyz"
chunk_size = 10
overlap = 3
stride = chunk_size - overlap  # 7

chunks = []
for i in range(0, len(text), stride):
    chunks.append(text[i:i+chunk_size])

assert len(chunks) == 4
assert chunks[0] == "abcdefghij"
assert chunks[1] == "hijklmnopq"  # 'hij' overlapping
assert chunks[0][-overlap:] == chunks[1][:overlap]
print(f"Chunks generated with 3-char overlap: {chunks}")

# -------------------------------------------- 2. Parent-Child Hierarchical Mapping
parent_chunk = "Database index internals: B-Trees balance height to maintain O(log N) lookup."
child_1 = "Database index internals"
child_2 = "B-Trees balance height to maintain O(log N) lookup."

parent_child_map = {101: parent_chunk, 102: parent_chunk}
assert parent_child_map[101] == parent_child_map[102]
print("Child chunks 101 and 102 successfully map to parent document context.")

# -------------------------------------------- 3. Token Count Boundary Guard
max_tokens = 512
chunk_tokens = 350
assert chunk_tokens <= max_tokens
print(f"Chunk verified within {max_tokens}-token embedding budget.")

print()
print("All checks passed.")
