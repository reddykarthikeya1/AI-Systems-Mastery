"""Beginner playground for Module 05 - Continuous & Dynamic Batching.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# -------------------------------------------- 1. Iteration-Level Scheduling vs Static Batching
active_requests = {"req_1": 2, "req_2": 5, "req_3": 1}  # Remaining tokens
finished = []

# One decode iteration
for rid in list(active_requests.keys()):
    active_requests[rid] -= 1
    if active_requests[rid] == 0:
        finished.append(rid)
        del active_requests[rid]

assert finished == ["req_3"]
assert "req_1" in active_requests and "req_2" in active_requests
print(f"Iteration finished requests: {finished}; slots immediately freed for new arrivals.")

# -------------------------------------------- 2. Padding Token Elimination
seq_lengths = [3, 5, 2]
static_padded_matrix_elements = max(seq_lengths) * len(seq_lengths)  # 5 * 3 = 15
continuous_flattened_elements = sum(seq_lengths)                     # 10
tokens_saved = static_padded_matrix_elements - continuous_flattened_elements

assert static_padded_matrix_elements == 15
assert continuous_flattened_elements == 10
assert tokens_saved == 5
print(f"Continuous batching eliminated {tokens_saved} wasteful padding tokens (33% compute saved).")

# -------------------------------------------- 3. GPU Utilization Saturation
max_capacity = 8
waiting_queue = deque(["req_4", "req_5"])
while len(active_requests) < max_capacity and waiting_queue:
    active_requests[waiting_queue.popleft()] = 4

assert len(active_requests) == 4
print(f"Active batch replenished to {len(active_requests)} requests.")

print()
print("All checks passed.")
