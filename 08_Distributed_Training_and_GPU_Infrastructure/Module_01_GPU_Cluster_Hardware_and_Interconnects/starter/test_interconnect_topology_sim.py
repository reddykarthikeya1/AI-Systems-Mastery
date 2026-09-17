"""Unit tests for Cluster Interconnect Topology Simulator."""

from __future__ import annotations

import pytest
from interconnect_topology_sim import ClusterTopologySimulator


def test_nvlink_faster_than_infiniband():
    tensor_bytes = 100 * 1024 * 1024
    nvlink_time = ClusterTopologySimulator.calculate_ring_allreduce_time(tensor_bytes, world_size=8, tier="nvlink4")
    ib_time = ClusterTopologySimulator.calculate_ring_allreduce_time(tensor_bytes, world_size=8, tier="infiniband_ndr")

    assert nvlink_time < ib_time
    assert nvlink_time * 5.0 < ib_time


def test_overlap_efficiency():
    eff_full = ClusterTopologySimulator.compute_overlap_efficiency(0.010, 0.010)
    assert eff_full == 1.0

    eff_half = ClusterTopologySimulator.compute_overlap_efficiency(0.005, 0.010)
    assert pytest.approx(eff_half, 0.01) == 0.5
