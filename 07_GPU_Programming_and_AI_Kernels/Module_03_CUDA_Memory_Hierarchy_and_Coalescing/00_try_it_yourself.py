"""Beginner playground for Module 03 - CUDA Memory Hierarchy & Coalescing.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Memory Latency Hierarchy
latencies = {"registers": 1, "shared_sram": 20, "global_dram": 300}
assert latencies["global_dram"] / latencies["registers"] == 300
assert latencies["shared_sram"] < latencies["global_dram"]
print(f"Memory latencies in cycles: {latencies}")

# -------------------------------------------- 2. Coalesced Memory Access Pattern
warp_size = 32
bytes_per_word = 4
transaction_size = 128  # bytes

# Coalesced: thread i accesses index i
coalesced_span = warp_size * bytes_per_word
transactions_needed = math.ceil(coalesced_span / transaction_size)

assert coalesced_span == 128
assert transactions_needed == 1
print(f"Coalesced warp access requires exactly {transactions_needed} memory transaction(s).")

# -------------------------------------------- 3. Strided Uncoalesced Memory Penalty
stride = 8
uncoalesced_span = warp_size * bytes_per_word * stride
transactions_strided = min(warp_size, math.ceil(uncoalesced_span / transaction_size))

assert transactions_strided > transactions_needed
assert transactions_strided == 8
print(f"Strided access (stride={stride}) burns {transactions_strided} transactions for same data.")

print()
print("All checks passed.")
