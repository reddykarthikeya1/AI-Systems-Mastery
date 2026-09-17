"""Beginner playground for Module 06 - Chunked Prefill & PD Disaggregation.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Chunked Prefill Token Budgeting
prompt_size = 1200
chunk_budget = 512
chunks = []
remaining = prompt_size
while remaining > 0:
    c = min(remaining, chunk_budget)
    chunks.append(c)
    remaining -= c

assert chunks == [512, 512, 176]
assert sum(chunks) == 1200
print(f"Prompt chunked into steps: {chunks}")

# -------------------------------------------- 2. Decoupled Inter-GPU KV Transfer
kv_cache_mb = 64.0
network_bw_gb_s = 50.0  # 400 Gbps InfiniBand
transfer_time_ms = (kv_cache_mb / (network_bw_gb_s * 1024)) * 1000

assert transfer_time_ms < 2.0
assert transfer_time_ms == 1.25
print(f"KV transfer time across network: {transfer_time_ms:.2f} ms (negligible latency).")

# -------------------------------------------- 3. Elimination of Decode Interference
tpot_without_disaggregation = [20, 21, 150, 20, 180]  # Spikes due to prefill preemption
tpot_with_disaggregation = [20, 21, 20, 21, 20]        # Smooth execution

assert max(tpot_with_disaggregation) == 21
assert max(tpot_without_disaggregation) == 180
print(f"P99 TPOT reduced from {max(tpot_without_disaggregation)} ms to {max(tpot_with_disaggregation)} ms.")

print()
print("All checks passed.")
