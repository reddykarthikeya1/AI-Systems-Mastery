"""Tests for Buffer Cache Clock Sweep."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_buffer_cache_clock_sweep import buffer_cache_clock_sweep
except ImportError:
    from p01_buffer_cache_clock_sweep import buffer_cache_clock_sweep


def test_buffer_cache_clock_sweep():
    frames = [
        {'page_id': 101, 'ref_bit': 1, 'dirty': False},
        {'page_id': 102, 'ref_bit': 0, 'dirty': False},
        {'page_id': 103, 'ref_bit': 1, 'dirty': True},
    ]
    evicted, hand = buffer_cache_clock_sweep(frames, 0)
    assert frames[0]['ref_bit'] == 0  # cleared
    assert evicted == 1               # frame 1 had ref_bit 0 and clean
    assert hand == 2
