"""Tests for Paged Kv Block Table."""
from __future__ import annotations

import pytest
from p01_paged_kv_block_table import paged_kv_block_table


def test_paged_kv_block_table():
    # Logical block 0 -> physical 42, logical block 1 -> physical 99
    table = [42, 99]
    assert paged_kv_block_table(table, 5, 16) == (42, 5)
    assert paged_kv_block_table(table, 20, 16) == (99, 4)
