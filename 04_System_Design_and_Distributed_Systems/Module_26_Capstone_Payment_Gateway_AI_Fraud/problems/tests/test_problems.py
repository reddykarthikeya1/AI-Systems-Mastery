"""Tests for Idempotent Payment Deduplication."""
from __future__ import annotations

import pytest
from p01_idempotent_payment_deduplication import idempotent_payment_deduplication


def test_idempotent_payment_deduplication():
    store = {}
    r1, is_replay1 = idempotent_payment_deduplication(store, 'order_xyz_123', {'amount': 99.95})
    assert is_replay1 is False
    assert r1['status'] == 'PAID'
    
    # Second call with same idempotency key
    r2, is_replay2 = idempotent_payment_deduplication(store, 'order_xyz_123', {'amount': 99.95})
    assert is_replay2 is True
    assert r2 == r1
