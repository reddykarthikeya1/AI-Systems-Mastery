"""Pytest suite for GPU Microarchitecture and Execution Model problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if Path.cwd().resolve() == PROB_DIR.resolve():
    if str(PROB_DIR) not in sys.path:
        sys.path.insert(0, str(PROB_DIR))
else:
    if str(SOL_DIR) not in sys.path:
        sys.path.insert(0, str(SOL_DIR))

from p01_calculate_tile_occupancy import calculate_tile_occupancy


def test_calculate_tile_occupancy():
    res = calculate_tile_occupancy(threads_per_block=256, shared_mem_bytes=16384)
    assert res["active_blocks"] == 6  # min(8, 6)
    assert res["active_warps"] == 48
    assert res["occupancy_percent"] == 75.0
    # Invalid thread count
    assert calculate_tile_occupancy(100, 0)["active_blocks"] == 0

