"""Pytest suite for Inference Latency Throughput Tradeoffs problem bank."""

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

from p01_simulate_prefix_cache_hit import simulate_prefix_cache_hit


def test_simulate_prefix_cache_hit():
    cached = [[1, 2, 3, 4, 5], [1, 2, 9, 10]]
    assert simulate_prefix_cache_hit(cached, [1, 2, 3, 4, 8]) == 4
    assert simulate_prefix_cache_hit(cached, [1, 2, 9, 11]) == 3
    assert simulate_prefix_cache_hit(cached, [7, 8, 9]) == 0
    assert simulate_prefix_cache_hit([], [1, 2]) == 0

