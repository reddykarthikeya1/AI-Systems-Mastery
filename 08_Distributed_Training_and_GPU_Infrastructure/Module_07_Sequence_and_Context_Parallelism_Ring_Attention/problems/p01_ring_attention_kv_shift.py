"""Problem 01 — Ring Attention Kv Shift

Topic: 07 Sequence and Context Parallelism Ring Attention
Target: Production-grade implementation

Determine source and destination ranks for ring attention KV chunk shift.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ring_attention_kv_shift(rank: int, world_size: int, step: int) -> tuple[int, int]:
    """In step `step` of ring attention:
    Rank sends its current KV chunk to (rank + 1) % world_size
    Rank receives KV chunk from (rank - 1 + world_size) % world_size
    Returns (send_to_rank, recv_from_rank).
    """
    raise NotImplementedError("Implement ring_attention_kv_shift")
