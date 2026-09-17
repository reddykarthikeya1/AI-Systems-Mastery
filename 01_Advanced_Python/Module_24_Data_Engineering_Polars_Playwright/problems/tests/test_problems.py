"""Tests for Single-Pass Rolling Mean & Max."""
from __future__ import annotations

import pytest
from p01_streaming_window_stats import rolling_window_stats


def test_streaming_window_stats():
    res = rolling_window_stats([1.0, 2.0, 3.0, 4.0], 2)
    assert res == [(1.5, 2.0), (2.5, 3.0), (3.5, 4.0)]
    assert rolling_window_stats([], 2) == []
