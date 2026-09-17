"""Tests for Sliding Idempotency Deduplicator."""
from __future__ import annotations

import pytest
from p01_idempotency_key_store import deduplicate_events


def test_deduplicate_events():
    stream = [('k1', 'val1'), ('k2', 'val2'), ('k1', 'val1_dup'), ('k3', 'val3')]
    assert deduplicate_events(stream) == [('k1', 'val1'), ('k2', 'val2'), ('k3', 'val3')]
    assert deduplicate_events([]) == []
