"""Unit tests for GPU Cluster Topology Simulator."""
from __future__ import annotations

import pytest
from cluster_topology_sim import (
    calculate_bisection_bandwidth,
    check_rail_alignment,
    estimate_transfer_time,
)


def test_bisection_bandwidth_scaling() -> None:
    # 64 nodes, 8 GPUs/node, 50 GB/s NICs, 1:1 non-blocking
    # 32 nodes per half * 8 GPUs * 50 GB/s = 12,800 GB/s (12.8 TB/s)
    bw = calculate_bisection_bandwidth(num_nodes=64, gpus_per_node=8, nic_bandwidth_gbs=50.0, oversubscription_ratio=1.0)
    assert pytest.approx(bw, rel=1e-5) == 12800.0

    # 2:1 oversubscribed fabric halves bisection bandwidth
    bw_oversub = calculate_bisection_bandwidth(num_nodes=64, gpus_per_node=8, nic_bandwidth_gbs=50.0, oversubscription_ratio=2.0)
    assert pytest.approx(bw_oversub, rel=1e-5) == 6400.0


def test_intra_vs_inter_node_transfer_latency() -> None:
    # 100 MB payload
    size = 100 * 1024 * 1024

    # Intra-node: (node 0, gpu 0) -> (node 0, gpu 1)
    intra_time = estimate_transfer_time((0, 0), (0, 1), size_bytes=size)

    # Inter-node: (node 0, gpu 0) -> (node 1, gpu 0)
    inter_time = estimate_transfer_time((0, 0), (1, 0), size_bytes=size)

    # Inter-node must be much slower due to InfiniBand 50 GB/s vs NVLink 900 GB/s
    assert inter_time > intra_time
    assert inter_time / intra_time > 10.0


def test_rail_alignment_check() -> None:
    # Both GPUs are index 3 -> rail-aligned
    assert check_rail_alignment(3, 3) is True
    # Different GPU index -> cross-rail traffic
    assert check_rail_alignment(2, 5) is False
