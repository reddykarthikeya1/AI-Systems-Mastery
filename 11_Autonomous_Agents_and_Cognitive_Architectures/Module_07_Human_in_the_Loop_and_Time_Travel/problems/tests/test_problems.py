"""Tests for Checkpoint Time Travel Fork."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_checkpoint_time_travel_fork import checkpoint_time_travel_fork
except ImportError:
    from p01_checkpoint_time_travel_fork import checkpoint_time_travel_fork


def test_checkpoint_time_travel_fork():
    hist = [
        {'checkpoint_id': 'cp1', 'state': {'turn': 1}},
        {'checkpoint_id': 'cp2', 'state': {'turn': 2}},
        {'checkpoint_id': 'cp3', 'state': {'turn': 3}},
    ]
    forked = checkpoint_time_travel_fork(hist, 'cp2')
    assert len(forked) == 2
    assert forked[-1]['checkpoint_id'] == 'cp2'
