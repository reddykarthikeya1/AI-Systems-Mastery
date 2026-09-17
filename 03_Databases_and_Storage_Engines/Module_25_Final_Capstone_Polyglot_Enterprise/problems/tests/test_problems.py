"""Tests for Change Data Capture Sync."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_change_data_capture_sync import change_data_capture_sync
except ImportError:
    from p01_change_data_capture_sync import change_data_capture_sync


def test_change_data_capture_sync():
    events = [
        {'op': 'UPDATE', 'account_id': 'A1', 'amount': 150.0, 'seq': 2},
        {'op': 'INSERT', 'account_id': 'A1', 'amount': 100.0, 'seq': 1},
        {'op': 'DELETE', 'account_id': 'A2', 'seq': 3}
    ]
    view = change_data_capture_sync(events, {'A2': 50.0})
    assert view == {'A1': 150.0}
