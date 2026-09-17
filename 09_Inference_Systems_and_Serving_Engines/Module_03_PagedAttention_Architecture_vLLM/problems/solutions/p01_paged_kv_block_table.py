"""Reference Solution — Problem 01: Paged Kv Block Table

Topic: 03 PagedAttention Architecture vLLM
"""

from __future__ import annotations


def paged_kv_block_table(block_table: list[int], token_index: int, block_size: int = 16) -> tuple[int, int]:
    logical_block = token_index // block_size
    offset = token_index % block_size
    return (block_table[logical_block], offset)
