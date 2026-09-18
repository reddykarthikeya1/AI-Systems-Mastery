"""Tests for Orchestrated Saga Coordinator."""
from __future__ import annotations

import pytest
from p01_orchestrated_saga_coordinator import orchestrated_saga_coordinator


def test_orchestrated_saga_coordinator():
    steps_ok = [
        {'name': 'reserve_flight', 'succeeds': True, 'compensate': 'cancel_flight'},
        {'name': 'reserve_hotel', 'succeeds': True, 'compensate': 'cancel_hotel'},
    ]
    ok, roll = orchestrated_saga_coordinator(steps_ok)
    assert ok is True and roll == []
    
    steps_fail = [
        {'name': 'reserve_flight', 'succeeds': True, 'compensate': 'cancel_flight'},
        {'name': 'reserve_hotel', 'succeeds': False, 'compensate': 'cancel_hotel'},
    ]
    ok2, roll2 = orchestrated_saga_coordinator(steps_fail)
    assert ok2 is False and roll2 == ['cancel_flight']
