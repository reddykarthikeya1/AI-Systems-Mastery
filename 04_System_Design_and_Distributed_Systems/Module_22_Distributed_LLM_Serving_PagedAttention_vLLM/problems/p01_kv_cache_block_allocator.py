"""Problem 01 — Kv Cache Block Allocator

Topic: 22 Distributed LLM Serving PagedAttention vLLM
Target: Production-grade implementation

Manage PagedAttention logical token blocks to physical GPU memory slots.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def kv_cache_block_allocator(block_size: int, requests: list[tuple[str, int]], total_physical_blocks: int) -> dict[str, list[int]]:
    """requests: list of (request_id, token_length).
    Each request requires ceil(token_length / block_size) physical blocks.
    Allocate physical blocks sequentially starting from block 0.
    If total required blocks exceed available physical blocks, raise MemoryError("Out of KV cache memory").
    Returns mapping request_id -> list of allocated physical block IDs.
    """
    raise NotImplementedError("Implement kv_cache_block_allocator")
