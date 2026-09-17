"""Tests for Memory Coalescing Detector."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_memory_coalescing_detector import memory_coalescing_detector
except ImportError:
    from p01_memory_coalescing_detector import memory_coalescing_detector


def test_memory_coalescing_detector():
    # Contiguous 32 floats (4 bytes each) = 128 bytes total -> 1 or 2 lines
    coalesced = [i * 4 for i in range(32)]
    assert memory_coalescing_detector(coalesced, 128) == 1
    # Strided access jumping 128 bytes each thread -> 32 cache lines!
    strided = [i * 128 for i in range(32)]
    assert memory_coalescing_detector(strided, 128) == 32
