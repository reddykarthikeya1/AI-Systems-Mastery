"""Tests for Elevator Dispatcher Scan."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_elevator_dispatcher_scan import elevator_dispatcher_scan
except ImportError:
    from p01_elevator_dispatcher_scan import elevator_dispatcher_scan


def test_elevator_dispatcher_scan():
    assert elevator_dispatcher_scan(5, 'UP', [2, 8, 3, 7, 5]) == [5, 7, 8, 3, 2]
    assert elevator_dispatcher_scan(5, 'DOWN', [2, 8, 3, 7]) == [3, 2, 7, 8]
