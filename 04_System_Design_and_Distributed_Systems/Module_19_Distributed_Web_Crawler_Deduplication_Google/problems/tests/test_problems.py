"""Tests for Simhash Near Duplicate Filter."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_simhash_near_duplicate_filter import simhash_near_duplicate_filter
except ImportError:
    from p01_simhash_near_duplicate_filter import simhash_near_duplicate_filter


def test_simhash_near_duplicate_filter():
    tokens1 = ["distributed", "crawler", "python", "systems", "dedup"]
    tokens2 = ["distributed", "crawler", "python", "systems", "dedup"]
    is_dup, d = simhash_near_duplicate_filter(tokens1, tokens2, 3)
    assert is_dup is True
    assert d == 0
