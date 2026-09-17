"""Reference Solution — Problem 01: Ring Attention Kv Shift

Topic: 07 Sequence and Context Parallelism Ring Attention
"""

from __future__ import annotations


def ring_attention_kv_shift(rank: int, world_size: int, step: int) -> tuple[int, int]:
    send_to = (rank + 1) % world_size
    recv_from = (rank - 1 + world_size) % world_size
    return (send_to, recv_from)
