"""Tests for Nvlink Switch Bandwidth Sim."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_nvlink_switch_bandwidth_sim import nvlink_switch_bandwidth_sim
except ImportError:
    from p01_nvlink_switch_bandwidth_sim import nvlink_switch_bandwidth_sim


def test_nvlink_switch_bandwidth_sim():
    # 1GB tensor over 900 GB/s NVLink
    t = nvlink_switch_bandwidth_sim(1024**3, 900 * 8, bus_efficiency=0.9)
    assert t > 0
    assert t < 5.0  # sub-5ms
