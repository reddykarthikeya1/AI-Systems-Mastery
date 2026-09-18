"""Problem 01 — Tma Asynchronous Transfer Schedule

Topic: 09 FlashAttention 3 and Hopper Blackwell Features
Target: Production-grade implementation

Schedule double-buffering pipeline stages for asynchronous TMA loads.

Example:
    >>> tma_asynchronous_transfer_schedule(3)
    [('LOAD', 0, 0), ('LOAD', 1, 1), ('COMPUTE', 0, 0), ('LOAD', 2, 0), ('COMPUTE', 1, 1), ('COMPUTE', 2, 0)]

Hints:
    Hint 1: Double-buffering means the load for tile `i` is issued while
        the compute for tile `i - 1` is still using the *other* buffer, so
        loads and computes for adjacent tiles interleave rather than run
        one-fully-after-another.
    Hint 2: Emit the schedule as one leading `('LOAD', 0, 0)`, then for each
        `i` from 1 to `total_tiles - 1` emit `('LOAD', i, i % 2)` followed
        by `('COMPUTE', i - 1, (i - 1) % 2)`, and finish with one trailing
        `('COMPUTE', total_tiles - 1, (total_tiles - 1) % 2)`.
    Hint 3: The buffer id is just the tile id mod 2 (only two physical
        buffers exist, so tile `i` and tile `i - 2` share one), and
        `total_tiles <= 0` must return an empty schedule rather than
        raising or emitting a lone LOAD with no matching COMPUTE.
"""

from __future__ import annotations


def tma_asynchronous_transfer_schedule(total_tiles: int) -> list[tuple[str, int, int]]:
    """Generate pipeline schedule for double-buffering (buffer 0 and 1):
    - First load: ('LOAD', tile 0, buffer 0)
    - For i in 1..total_tiles-1:
        ('LOAD', tile i, buffer i % 2)
        ('COMPUTE', tile i-1, buffer (i-1) % 2)
    - Last compute: ('COMPUTE', tile total_tiles-1, buffer (total_tiles-1) % 2)
    Returns schedule list of (action, tile_id, buffer_id).
    """
    raise NotImplementedError("Implement tma_asynchronous_transfer_schedule")
