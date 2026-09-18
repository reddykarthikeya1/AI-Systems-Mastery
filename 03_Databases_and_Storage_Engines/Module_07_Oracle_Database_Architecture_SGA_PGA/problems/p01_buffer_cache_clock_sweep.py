"""Problem 01 — Buffer Cache Clock Sweep

Topic: 07 Oracle Database Architecture SGA PGA
Target: Production-grade implementation

Second-chance clock sweep page eviction for database buffer pool.

Example:
    >>> frames = [
    ...     {'page_id': 101, 'ref_bit': 1, 'dirty': False},
    ...     {'page_id': 102, 'ref_bit': 0, 'dirty': False},
    ...     {'page_id': 103, 'ref_bit': 1, 'dirty': True},
    ... ]
    >>> buffer_cache_clock_sweep(frames, 0)
    (1, 2)

Hints:
    Hint 1: The clock hand only gives a frame a "second chance" when its
        ref_bit is set — it doesn't matter whether that frame is dirty or
        clean, a set ref_bit alone is enough to spare it this sweep.
    Hint 2: This is a circular scan: walk the frames list starting at hand
        and wrapping with modulo arithmetic, clearing ref_bit as you pass
        over set ones, until you land on a frame that is both ref_bit == 0
        and not dirty.
    Hint 3: Bound the scan (e.g. at 2 * len(frames) + 1 steps) so a buffer
        pool where every frame is dirty or perpetually re-referenced doesn't
        loop forever — in that unevictable case return (-1, hand) instead;
        otherwise return (evicted_index, hand advanced one past the
        eviction) so the next sweep resumes where this one left off.
"""

from __future__ import annotations


def buffer_cache_clock_sweep(frames: list[dict], hand: int) -> tuple[int, int]:
    """Each frame has: {'page_id': int, 'ref_bit': int, 'dirty': bool}.
    Scans from `hand`. If ref_bit == 1, set ref_bit = 0 and advance hand.
    If ref_bit == 0 and not dirty, evict this frame and return (evicted_index, new_hand).
    If all are ref_bit == 1 or dirty, continue circling until an evictable frame is found.
    """
    raise NotImplementedError("Implement buffer_cache_clock_sweep")
