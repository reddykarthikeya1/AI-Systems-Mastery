"""Tests for Ring Attention Kv Shift."""
from __future__ import annotations

import pytest
from p01_ring_attention_kv_shift import ring_attention_kv_shift


def test_ring_attention_kv_shift():
    send, recv = ring_attention_kv_shift(0, 4, 1)
    assert send == 1 and recv == 3
