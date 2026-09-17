"""Problem 01 — Memory Coalescing Detector

Topic: 03 CUDA Memory Hierarchy and Coalescing
Target: Production-grade implementation

Determine number of 128-byte cache lines needed to serve warp memory transaction addresses.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def memory_coalescing_detector(byte_addresses: list[int], cache_line_bytes: int = 128) -> int:
    """byte_addresses: list of byte memory addresses accessed by warp threads.
    Return number of distinct cache_line_bytes segments required to cover all addresses.
    """
    raise NotImplementedError("Implement memory_coalescing_detector")
