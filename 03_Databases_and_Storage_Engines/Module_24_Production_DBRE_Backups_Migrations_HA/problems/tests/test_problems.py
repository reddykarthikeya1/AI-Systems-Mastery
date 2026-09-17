"""Tests for Point In Time Recovery."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_point_in_time_recovery import point_in_time_recovery
except ImportError:
    from p01_point_in_time_recovery import point_in_time_recovery


def test_point_in_time_recovery():
    base = {'k1': 'v1_initial', 'k2': 'v2_initial'}
    wal = [
        (100, 'k1', 'v1_updated'),
        (200, 'k2', 'v2_updated'),
        (300, 'k1', 'v1_corrupted')  # after target_ts
    ]
    recovered = point_in_time_recovery(base, wal, target_ts=250)
    assert recovered['k1'] == 'v1_updated'
    assert recovered['k2'] == 'v2_updated'
