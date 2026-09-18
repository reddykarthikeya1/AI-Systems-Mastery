"""Tests for Deterministic Audit Trigger."""
from __future__ import annotations

import pytest
from p01_deterministic_audit_trigger import deterministic_audit_trigger


def test_deterministic_audit_trigger():
    audit = deterministic_audit_trigger('UPDATE', {'salary': 5000, 'dept': 'Eng'}, {'salary': 6000, 'dept': 'Eng'})
    assert audit['action'] == 'UPDATE'
    assert audit['delta'] == {'salary': (5000, 6000)}
    assert audit['timestamp_token'] == 'DETERMINISTIC_COMMIT'
