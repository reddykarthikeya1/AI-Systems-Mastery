"""Beginner playground for Module 09 - Context Optimization & NIAH Testing.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Needle In A Haystack (NIAH) Placement
haystack_tokens = ["the", "quick", "brown", "fox"] * 25  # 100 tokens
needle = "SECRET_PASSWORD_123"
depth_pct = 0.50  # 50% depth

insert_idx = int(len(haystack_tokens) * depth_pct)
haystack_with_needle = haystack_tokens[:insert_idx] + [needle] + haystack_tokens[insert_idx:]

assert haystack_with_needle[insert_idx] == needle
assert len(haystack_with_needle) == 101
print(f"Needle successfully inserted at index {insert_idx} ({depth_pct*100:.0f}% depth).")

# -------------------------------------------- 2. Lost in the Middle Phenomenon
accuracy_by_depth = {0.0: 0.98, 0.25: 0.85, 0.50: 0.72, 0.75: 0.84, 1.0: 0.99}

assert accuracy_by_depth[0.50] < accuracy_by_depth[0.0]
assert accuracy_by_depth[0.50] < accuracy_by_depth[1.0]
assert accuracy_by_depth[1.0] > 0.95
print(f"U-shaped accuracy curve: start={accuracy_by_depth[0.0]}, middle={accuracy_by_depth[0.50]}, end={accuracy_by_depth[1.0]}")

# -------------------------------------------- 3. Context Window Reordering
retrieved_passages = ["doc_3", "doc_2", "doc_1"]
# Put most relevant at beginning and second most at end
optimized_context = [retrieved_passages[2], retrieved_passages[0], retrieved_passages[1]]

assert optimized_context[0] == "doc_1"
assert len(optimized_context) == 3
print(f"Optimized context layout: {optimized_context}")

print()
print("All checks passed.")
