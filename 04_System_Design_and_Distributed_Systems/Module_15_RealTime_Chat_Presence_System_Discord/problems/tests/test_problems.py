"""Tests for Heartbeat Presence Tracker."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_heartbeat_presence_tracker import heartbeat_presence_tracker
except ImportError:
    from p01_heartbeat_presence_tracker import heartbeat_presence_tracker


def test_heartbeat_presence_tracker():
    hb = {'u1': 100, 'u2': 80, 'u3': 60}
    online, expired = heartbeat_presence_tracker(hb, 110, 30)
    assert online == {'u1', 'u2'}
    assert expired == {'u3'}
