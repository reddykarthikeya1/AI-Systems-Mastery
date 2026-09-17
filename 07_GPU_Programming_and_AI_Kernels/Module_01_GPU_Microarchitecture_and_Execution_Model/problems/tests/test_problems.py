"""Tests for Warp Divergence Metrics."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_warp_divergence_metrics import warp_divergence_metrics
except ImportError:
    from p01_warp_divergence_metrics import warp_divergence_metrics


def test_warp_divergence_metrics():
    # 2 diverged paths, each with 16 threads active out of 32
    mask1 = (1 << 16) - 1
    mask2 = ((1 << 16) - 1) << 16
    cycles, eff = warp_divergence_metrics([mask1, mask2], 32)
    assert cycles == 2
    assert eff == 0.5
