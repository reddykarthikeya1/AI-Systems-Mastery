"""Tests for Back Of Envelope Capacity."""
from __future__ import annotations

import pytest
from p01_back_of_envelope_capacity import back_of_envelope_capacity


def test_back_of_envelope_capacity():
    res = back_of_envelope_capacity(10_000_000, 20, 0.9, 500)
    assert res['read_qps'] > 0
    assert res['write_qps'] > 0
    assert res['daily_storage_gb'] > 0
