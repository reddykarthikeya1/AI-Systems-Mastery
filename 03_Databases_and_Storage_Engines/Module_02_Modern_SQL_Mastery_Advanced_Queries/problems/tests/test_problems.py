"""Pytest suite for Modern SQL Mastery Advanced Queries problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if str(SOL_DIR) not in sys.path:
    sys.path.insert(0, str(SOL_DIR))

from p01_compute_storage_layout import compute_storage_layout


def test_compute_storage_layout():
    records = [1000, 2000, 1500, 3000]
    layout = compute_storage_layout(records, block_size=4096)
    assert layout[0] == (0, 0)
    assert layout[1] == (0, 1000)
    assert layout[2] == (1, 0)  # 1000+2000+1500 = 4500 > 4096 -> next block
    assert layout[3] == (2, 0)
    assert compute_storage_layout([], 4096) == []

