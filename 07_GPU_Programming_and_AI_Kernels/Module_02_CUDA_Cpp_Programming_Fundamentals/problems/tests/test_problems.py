"""Tests for Grid Block Thread Indexer."""
from __future__ import annotations

import pytest
from p01_grid_block_thread_indexer import grid_block_thread_indexer


def test_grid_block_thread_indexer():
    assert grid_block_thread_indexer(2, 256, 10) == 522
    assert grid_block_thread_indexer(0, 128, 0) == 0
