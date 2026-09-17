"""Tests for Fanout On Write Feed."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_fanout_on_write_feed import fanout_on_write_feed
except ImportError:
    from p01_fanout_on_write_feed import fanout_on_write_feed


def test_fanout_on_write_feed():
    res1 = fanout_on_write_feed("regular_user", "post_1", ["f1", "f2"], 5)
    assert res1 == {"f1": ["post_1"], "f2": ["post_1"]}
    res2 = fanout_on_write_feed("celebrity", "post_2", ["f1", "f2", "f3", "f4", "f5", "f6"], 5)
    assert res2 == {"celebrity": ["post_2"]}
