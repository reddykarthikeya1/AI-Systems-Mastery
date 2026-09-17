"""Beginner playground for Module 02 - KV Cache Memory Management.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. KV Cache Bytes per Token Formula
n_layers = 32
n_heads = 32
d_head = 128
bytes_per_elem = 2  # FP16

# 2 for Key and Value
bytes_per_token = 2 * n_layers * n_heads * d_head * bytes_per_elem

assert bytes_per_token == 524_288  # Exactly 0.5 MB per token!
assert bytes_per_token == 512 * 1024
print(f"KV Cache memory footprint: {bytes_per_token / 1024:.0f} KB per token.")

# -------------------------------------------- 2. Multi-Query (MQA) and Grouped-Query (GQA) Savings
num_query_heads = 32
num_kv_heads_gqa = 8  # Group of 4
gqa_ratio = num_query_heads / num_kv_heads_gqa
gqa_bytes_per_token = bytes_per_token / gqa_ratio

assert gqa_ratio == 4.0
assert gqa_bytes_per_token == 131_072  # 128 KB per token
print(f"GQA (4:1) cuts KV cache from {bytes_per_token / 1024:.0f} KB down to {gqa_bytes_per_token / 1024:.0f} KB per token.")

# -------------------------------------------- 3. Maximum Sequence Capacity Calculation
available_vram_gb = 40.0
total_tokens_capacity = (available_vram_gb * (1024**3)) / gqa_bytes_per_token

assert total_tokens_capacity > 300_000
assert int(total_tokens_capacity) == 327_680
print(f"Supported KV capacity: {int(total_tokens_capacity):,} tokens across all concurrent sessions.")

print()
print("All checks passed.")
