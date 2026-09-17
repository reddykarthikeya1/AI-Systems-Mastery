"""Problem 01 — Paged Kv Block Table

Topic: 03 PagedAttention Architecture vLLM
Target: Production-grade implementation

Translate logical token position to physical block ID and intra-block offset.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def paged_kv_block_table(block_table: list[int], token_index: int, block_size: int = 16) -> tuple[int, int]:
    """Map token_index to (physical_block_id, block_offset).
    logical_block_number = token_index // block_size
    physical_block_id = block_table[logical_block_number]
    block_offset = token_index % block_size
    """
    raise NotImplementedError("Implement paged_kv_block_table")
