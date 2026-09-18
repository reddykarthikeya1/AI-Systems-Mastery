"""Tests for Wal Checkpoint Merge."""
from __future__ import annotations

import pytest
from p01_wal_checkpoint_merge import wal_checkpoint_merge


def test_wal_checkpoint_merge():
    pages = {1: b"page1_v0", 2: b"page2_v0"}
    frames = [
        (1, 1, b"page1_v1", False),
        (2, 2, b"page2_v1", True),  # Commit tx1
        (3, 1, b"page1_uncommitted", False)  # Uncommitted
    ]
    merged = wal_checkpoint_merge(pages, frames)
    assert merged[1] == b"page1_v1"
    assert merged[2] == b"page2_v1"
