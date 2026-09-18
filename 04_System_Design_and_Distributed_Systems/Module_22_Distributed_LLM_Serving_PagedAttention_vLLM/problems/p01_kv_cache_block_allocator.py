"""Problem 01 — Kv Cache Block Allocator

Topic: 22 Distributed LLM Serving PagedAttention vLLM
Target: Production-grade implementation

Manage PagedAttention logical token blocks to physical GPU memory slots.

Example:
    >>> kv_cache_block_allocator(16, [('req_1', 32), ('req_2', 17)], total_physical_blocks=10)
    {'req_1': [0, 1], 'req_2': [2, 3]}

Hints:
    Hint 1: This is bump-pointer allocation -- each request claims the
        next contiguous run of block IDs, and nothing is ever freed or
        reused within a single call.
    Hint 2: Track a running `next_block` cursor; for each request compute
        the block count with `math.ceil(token_length / block_size)`,
        assign `range(next_block, next_block + needed)`, then advance the
        cursor by `needed`.
    Hint 3: 17 tokens with `block_size=16` needs 2 blocks, not 1 --
        `ceil(17 / 16) == 2` -- so plain `//` division under-allocates and
        must not be used; once a request's needed blocks would push the
        running total past `total_physical_blocks`, raise
        `MemoryError("Out of KV cache memory")` for that request instead
        of partially allocating it.
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
