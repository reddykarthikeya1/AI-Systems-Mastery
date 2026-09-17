"""Beginner playground for Module 03 - PagedAttention Architecture (vLLM).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Virtual Memory Block Mapping
block_size = 16
logical_token_index = 37

logical_block_num = logical_token_index // block_size
block_offset = logical_token_index % block_size

assert logical_block_num == 2  # Block 2
assert block_offset == 5       # 5th token in block 2
assert logical_block_num * block_size + block_offset == 37
print(f"Token {logical_token_index} maps to Block {logical_block_num}, Offset {block_offset}.")

# -------------------------------------------- 2. Zero Internal Fragmentation Invariant
max_seq_len = 4096
actual_tokens = 150
static_waste = (max_seq_len - actual_tokens) / max_seq_len
paged_blocks_used = math.ceil(actual_tokens / block_size)  # 10 blocks = 160 slots
paged_waste = (paged_blocks_used * block_size - actual_tokens) / (paged_blocks_used * block_size)

assert static_waste > 0.90
assert paged_waste < 0.10
print(f"Memory waste: Static reservation={static_waste:.1%}, PagedAttention={paged_waste:.1%}")

# -------------------------------------------- 3. Copy-On-Write Fork for Parallel Sampling
block_ref_counts = {101: 1}
# Fork 2 sampling branches
block_ref_counts[101] += 2

assert block_ref_counts[101] == 3, "Prompt block shared by parent and 2 child streams"
print(f"Physical block 101 shared with ref_count={block_ref_counts[101]}; zero redundant prompt memory.")

print()
print("All checks passed.")
