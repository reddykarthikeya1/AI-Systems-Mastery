"""Reference Solution — Problem 01: Memory Coalescing Detector

Topic: 03 CUDA Memory Hierarchy and Coalescing
"""

from __future__ import annotations


def memory_coalescing_detector(byte_addresses: list[int], cache_line_bytes: int = 128) -> int:
    segments = set(addr // cache_line_bytes for addr in byte_addresses)
    return len(segments)
