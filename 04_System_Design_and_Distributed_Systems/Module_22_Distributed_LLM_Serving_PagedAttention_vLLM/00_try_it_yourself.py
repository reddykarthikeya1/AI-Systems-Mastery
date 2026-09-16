"""Beginner playground for Module 22 - Distributed LLM Serving and PagedAttention.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ----------------------- 1. What the KV cache is, and why it dominates memory
KV_BYTES_PER_TOKEN = 800_000          # a realistic figure for a mid-size model
MAX_CONTEXT = 2_048
GPU_MEMORY = 40_000_000_000           # 40 GB

full_reservation = MAX_CONTEXT * KV_BYTES_PER_TOKEN
print(f"reserving the full context costs {full_reservation / 1e9:.2f} GB per request")
assert full_reservation > 1e9


# ---------------- 2. Reserve for the worst case and you waste the common case
REQUEST_LENGTHS = [120, 200, 340, 150, 90, 600, 210, 180]

contiguous_slots = GPU_MEMORY // full_reservation
reserved = len(REQUEST_LENGTHS) * full_reservation
actually_used = sum(REQUEST_LENGTHS) * KV_BYTES_PER_TOKEN
waste = 1 - actually_used / reserved

print(f"concurrent requests that fit: {contiguous_slots}")
print(f"memory reserved: {reserved / 1e9:>6.2f} GB")
print(f"memory used:     {actually_used / 1e9:>6.2f} GB")
print(f"wasted:          {waste:.0%}")
assert waste > 0.8, "most of the most expensive memory in the building is idle"


# ------------------------------ 3. Pages: allocate in small blocks, on demand
BLOCK_TOKENS = 16


def blocks_for(tokens):
    return -(-tokens // BLOCK_TOKENS)      # ceiling division


paged_bytes = sum(blocks_for(n) * BLOCK_TOKENS for n in REQUEST_LENGTHS)
paged_bytes *= KV_BYTES_PER_TOKEN
paged_waste = 1 - actually_used / paged_bytes

print(f"paged allocation uses {paged_bytes / 1e9:.2f} GB for the same 8 requests")
print(f"wasted: {paged_waste:.1%} (only the tail of each last block)")
assert paged_waste < 0.05, "internal fragmentation is now under 5%"
assert paged_bytes < reserved / 8, "8x less memory for identical work"


# ------------------------------- 4. The payoff: how many requests fit at once
average_tokens = sum(REQUEST_LENGTHS) / len(REQUEST_LENGTHS)
contiguous_capacity = GPU_MEMORY // full_reservation
paged_capacity = GPU_MEMORY // (blocks_for(average_tokens) * BLOCK_TOKENS
                                * KV_BYTES_PER_TOKEN)

print(f"contiguous allocation: {contiguous_capacity:>4} concurrent sequences")
print(f"paged allocation:      {paged_capacity:>4} concurrent sequences")
print(f"improvement: {paged_capacity / contiguous_capacity:.1f}x")
assert paged_capacity > contiguous_capacity * 5
print("Same GPU, same model, same weights. Different allocator.")


# -------------------------- 5. Continuous batching, the other half of the win
batch = [5, 5, 5, 100]                      # tokens left to generate
waiting = [5, 5, 5]

static_steps = max(batch)
print(f"static batching: {static_steps} steps, "
      f"and 3 slots idle for {static_steps - 5} of them")

slots = list(batch)
queue = list(waiting)
steps = 0
while any(slots) or queue:
    steps += 1
    for i, remaining in enumerate(slots):
        if remaining > 0:
            slots[i] -= 1
        elif queue:
            slots[i] = queue.pop(0) - 1
    if not queue and not any(slots):
        break

static_for_everything = static_steps + max(waiting)
print(f"continuous batching: {steps} steps for all {len(batch) + len(waiting)} requests")
print(f"static batching would need {static_for_everything} steps for the same seven")
assert steps < static_for_everything, "the waiting requests fitted into the idle gaps"


print()
print("All checks passed.")
