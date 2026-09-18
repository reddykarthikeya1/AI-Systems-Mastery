"""Problem 01 — Paged Kv Block Table

Topic: 03 PagedAttention Architecture vLLM
Target: Production-grade implementation

Translate logical token position to physical block ID and intra-block offset.

Example:
    >>> paged_kv_block_table([42, 99], 20, 16)
    (99, 4)

Hints:
    Hint 1: This is PagedAttention's core trick — token positions are
        logically contiguous, but the KV blocks backing them are scattered
        in physical memory, so split `token_index` into "which block" and
        "where inside that block" before touching `block_table` at all.
    Hint 2: Use integer floor division and modulo (equivalently `divmod`) on
        `token_index` by `block_size` to get the logical block number and
        the intra-block offset.
    Hint 3: `block_table` maps LOGICAL block numbers (0, 1, 2, ...) to
        arbitrary PHYSICAL block ids, so `token_index // block_size` is only
        an index into `block_table` — the looked-up id itself can be any
        value (e.g. 99), and the return order must stay
        `(physical_block_id, block_offset)`, not the reverse.
"""

from __future__ import annotations


def paged_kv_block_table(block_table: list[int], token_index: int, block_size: int = 16) -> tuple[int, int]:
    """Map token_index to (physical_block_id, block_offset).
    logical_block_number = token_index // block_size
    physical_block_id = block_table[logical_block_number]
    block_offset = token_index % block_size
    """
    raise NotImplementedError("Implement paged_kv_block_table")
