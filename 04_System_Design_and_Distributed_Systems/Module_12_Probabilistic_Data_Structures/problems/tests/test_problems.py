"""Tests for Count Min Sketch Heavy Hitters."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_count_min_sketch_heavy_hitters import count_min_sketch_heavy_hitters
except ImportError:
    from p01_count_min_sketch_heavy_hitters import count_min_sketch_heavy_hitters


def test_count_min_sketch_heavy_hitters():
    stream = ["apple"] * 10 + ["banana"] * 2 + ["orange"] * 1
    heavy = count_min_sketch_heavy_hitters(stream, width=50, depth=4, threshold=5)
    assert "apple" in heavy
    assert "banana" not in heavy
