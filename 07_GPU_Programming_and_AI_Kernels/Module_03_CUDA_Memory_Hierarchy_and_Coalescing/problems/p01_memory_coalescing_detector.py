"""Problem 01 — Memory Coalescing Detector

Topic: 03 CUDA Memory Hierarchy and Coalescing
Target: Production-grade implementation

Determine number of 128-byte cache lines needed to serve warp memory transaction addresses.

Example:
    >>> memory_coalescing_detector([0, 4, 8, 200, 260], 128)
    3

Hints:
    Hint 1: What matters isn't the raw addresses but which aligned segment
        each one lands in — the number of distinct segments touched is the
        number of memory transactions the warp must issue.
    Hint 2: Integer-divide each address by `cache_line_bytes` to get its
        segment id, then count how many distinct segment ids appear (a
        `set` comprehension is the natural fit).
    Hint 3: Order and duplicate addresses don't matter, only distinctness.
        A fully contiguous run of addresses within one 128-byte window
        collapses to a single segment, while a stride equal to
        `cache_line_bytes` puts every thread in its own segment — the
        worst case the tests check for.
"""

from __future__ import annotations


def memory_coalescing_detector(byte_addresses: list[int], cache_line_bytes: int = 128) -> int:
    """byte_addresses: list of byte memory addresses accessed by warp threads.
    Return number of distinct cache_line_bytes segments required to cover all addresses.
    """
    raise NotImplementedError("Implement memory_coalescing_detector")
