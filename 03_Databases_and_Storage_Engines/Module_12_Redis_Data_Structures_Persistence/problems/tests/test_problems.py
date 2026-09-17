"""Tests for Rdb Snapshot Ziplist."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_rdb_snapshot_ziplist import rdb_snapshot_ziplist
except ImportError:
    from p01_rdb_snapshot_ziplist import rdb_snapshot_ziplist


def test_rdb_snapshot_ziplist():
    res = rdb_snapshot_ziplist(["redis", 42, "cache"])
    assert len(res) > 6
    total_len = int.from_bytes(res[:4], 'big')
    count = int.from_bytes(res[4:6], 'big')
    assert total_len == len(res)
    assert count == 3
