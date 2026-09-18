"""Tests for Mvcc Tuple Visibility."""
from __future__ import annotations

import pytest
from p01_mvcc_tuple_visibility import mvcc_tuple_visibility


def test_mvcc_tuple_visibility():
    # snapshot: min=100, max=105, active={102, 104}
    active = {102, 104}
    # Created before snapshot_xmin (committed) and not deleted
    assert mvcc_tuple_visibility(90, None, 100, 105, active) is True
    # Created by active tx
    assert mvcc_tuple_visibility(102, None, 100, 105, active) is False
    # Created in future
    assert mvcc_tuple_visibility(106, None, 100, 105, active) is False
    # Deleted by committed tx 95
    assert mvcc_tuple_visibility(90, 95, 100, 105, active) is False
