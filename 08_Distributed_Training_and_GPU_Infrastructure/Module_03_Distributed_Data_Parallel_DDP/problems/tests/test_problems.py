"""Pytest suite for Distributed Data Parallel DDP problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if str(SOL_DIR) not in sys.path:
    sys.path.insert(0, str(SOL_DIR))

from p01_compute_ring_allreduce_cost import compute_ring_allreduce_cost


def test_compute_ring_allreduce_cost():
    res = compute_ring_allreduce_cost(param_bytes=1000000, world_size=4, bus_bandwidth_gbps=100.0)
    assert res["comm_bytes"] == 2.0 * (3.0 / 4.0) * 1000000  # 1,500,000
    assert res["time_ms"] > 0.0
    assert compute_ring_allreduce_cost(1000, 1, 100.0)["comm_bytes"] == 0.0

