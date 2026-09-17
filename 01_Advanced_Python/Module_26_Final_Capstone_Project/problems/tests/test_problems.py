"""Tests for Circuit Breaker State Machine."""
from __future__ import annotations

import pytest
from p01_circuit_breaker_states import CircuitBreaker


def test_circuit_breaker_states():
    cb = CircuitBreaker(failure_threshold=2)
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.state == 'OPEN'
    assert cb.allow_request() is False
    cb.record_success()
    assert cb.state == 'CLOSED'
    assert cb.allow_request() is True
