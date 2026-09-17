"""Tests for Memoization Closure with TTL."""
from __future__ import annotations

import pytest
from p01_memoize_with_ttl import memoize_with_ttl


def test_memoize_with_ttl():
    count = 0
    @memoize_with_ttl(10.0)
    def inc(x):
        nonlocal count
        count += 1
        return x + 1
    assert inc(2) == 3
    assert inc(2) == 3
    assert count == 1
    assert inc.stats['hits'] == 1
    assert inc.stats['misses'] == 1
