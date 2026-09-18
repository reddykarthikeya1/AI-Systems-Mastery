"""Problem 01 — Ring Attention Kv Shift

Topic: 07 Sequence and Context Parallelism Ring Attention
Target: Production-grade implementation

Determine source and destination ranks for ring attention KV chunk shift.

Example:
    >>> ring_attention_kv_shift(0, 4, 1)
    (1, 3)

Hints:
    Hint 1: Ranks are arranged in a logical ring, so "next" and "previous"
        neighbor are just one position clockwise and counter-clockwise,
        wrapping back around at the ends of the ring.
    Hint 2: Compute the next neighbor with modular arithmetic, `(rank + 1) %
        world_size`, and the previous neighbor the same way but shifted
        back and re-offset before the modulo: `(rank - 1 + world_size) %
        world_size`.
    Hint 3: Adding `world_size` before taking `%` is what keeps the
        previous-rank computation correct when `rank == 0` (Python's `%`
        already returns a non-negative result for a positive modulus, but
        the `+ world_size` makes that explicit and is worth keeping). Note
        `step` doesn't change who the neighbors are — every step shifts by
        exactly one ring position — so it isn't used in the formula at all.
"""

from __future__ import annotations


def ring_attention_kv_shift(rank: int, world_size: int, step: int) -> tuple[int, int]:
    """In step `step` of ring attention:
    Rank sends its current KV chunk to (rank + 1) % world_size
    Rank receives KV chunk from (rank - 1 + world_size) % world_size
    Returns (send_to_rank, recv_from_rank).
    """
    raise NotImplementedError("Implement ring_attention_kv_shift")
