"""Tests for LFU Cache Eviction Frequency Counter."""
from __future__ import annotations

import pytest
from p01_lfu_cache_evictor import lfu_eviction_candidate


def test_lfu_eviction_candidate():
    freqs = {'a': 3, 'b': 1, 'c': 1}
    order = ['c', 'b', 'a']  # c was accessed earlier than b
    assert lfu_eviction_candidate(freqs, order) == 'c'
    assert lfu_eviction_candidate({}, []) is None
