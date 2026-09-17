"""Reference Solution — Problem 01: Kv Cache Block Allocator

Topic: 22 Distributed LLM Serving PagedAttention vLLM
"""

from __future__ import annotations


def kv_cache_block_allocator(block_size: int, requests: list[tuple[str, int]], total_physical_blocks: int) -> dict[str, list[int]]:
    import math
    allocated = {}
    next_block = 0
    for req_id, tokens in requests:
        needed = math.ceil(tokens / block_size)
        if next_block + needed > total_physical_blocks:
            raise MemoryError("Out of KV cache memory")
        allocated[req_id] = list(range(next_block, next_block + needed))
        next_block += needed
    return allocated
