"""Problem 01 — Buffer Cache Clock Sweep

Topic: 07 Oracle Database Architecture SGA PGA
Target: Production-grade implementation

Second-chance clock sweep page eviction for database buffer pool.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def buffer_cache_clock_sweep(frames: list[dict], hand: int) -> tuple[int, int]:
    """Each frame has: {'page_id': int, 'ref_bit': int, 'dirty': bool}.
    Scans from `hand`. If ref_bit == 1, set ref_bit = 0 and advance hand.
    If ref_bit == 0 and not dirty, evict this frame and return (evicted_index, new_hand).
    If all are ref_bit == 1 or dirty, continue circling until an evictable frame is found.
    """
    raise NotImplementedError("Implement buffer_cache_clock_sweep")
