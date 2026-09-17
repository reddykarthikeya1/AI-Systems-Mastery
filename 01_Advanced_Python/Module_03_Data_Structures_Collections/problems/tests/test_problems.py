"""Tests for LRU Key Eviction Order."""
from __future__ import annotations

import pytest
from p01_lru_cache_list import lru_cache_list


def test_lru_cache_list():
    ops = [('set', 'a'), ('set', 'b'), ('get', 'a'), ('set', 'c')]
    assert lru_cache_list(2, ops) == ['a', 'c']
    assert lru_cache_list(1, [('set', 'x'), ('set', 'y')]) == ['y']
