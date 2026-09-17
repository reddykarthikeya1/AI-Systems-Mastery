"""Tests for Geohash Proximity Search."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_geohash_proximity_search import geohash_proximity_search
except ImportError:
    from p01_geohash_proximity_search import geohash_proximity_search


def test_geohash_proximity_search():
    drivers = {
        "d1": "9q8yy1",
        "d2": "9q8yy9",
        "d3": "9q8zaa",
        "d4": "8k1111"
    }
    matched = geohash_proximity_search("9q8yy0", drivers, 5)
    assert matched == ["d1", "d2"]
