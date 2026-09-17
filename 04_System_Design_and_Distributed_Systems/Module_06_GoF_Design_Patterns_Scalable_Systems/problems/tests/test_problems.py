"""Tests for Circuit Breaker State Machine."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_circuit_breaker_state_machine import circuit_breaker_state_machine
except ImportError:
    from p01_circuit_breaker_state_machine import circuit_breaker_state_machine


def test_circuit_breaker_state_machine():
    events = [
        ('FAILURE', 10),
        ('FAILURE', 11),
        ('FAILURE', 12),  # trips to OPEN
        ('SUCCESS', 80),  # ts 80 >= 12 + 60 -> HALF_OPEN, then SUCCESS -> CLOSED
    ]
    states = circuit_breaker_state_machine(events, 3, 60)
    assert states == ['CLOSED', 'CLOSED', 'OPEN', 'CLOSED']
