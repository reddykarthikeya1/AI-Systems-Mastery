"""Tests for Binlog Gtid Reconciliation."""
from __future__ import annotations

import pytest
from p01_binlog_gtid_reconciliation import binlog_gtid_reconciliation


def test_binlog_gtid_reconciliation():
    primary = [(1, 10), (15, 20)]
    replica = [(1, 8), (17, 18)]
    diff = binlog_gtid_reconciliation(primary, replica)
    assert diff == [(9, 10), (15, 16), (19, 20)]
    assert binlog_gtid_reconciliation([(1, 5)], [(1, 5)]) == []
