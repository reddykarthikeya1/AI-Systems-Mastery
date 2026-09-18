"""Tests for Lsm Leveled Compaction."""
from __future__ import annotations

import pytest
from p01_lsm_leveled_compaction import lsm_leveled_compaction


def test_lsm_leveled_compaction():
    run1 = [("k1", "v1_old", 10), ("k2", "v2", 15)]
    run2 = [("k1", "v1_new", 20), ("k2", None, 25)]  # k2 tombstone
    res = lsm_leveled_compaction([run1, run2])
    assert res == [("k1", "v1_new")]
