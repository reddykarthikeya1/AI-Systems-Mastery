"""Reference Solution — Problem 01: Nvlink Switch Bandwidth Sim

Topic: 01 GPU Cluster Hardware and Interconnects
"""

from __future__ import annotations


def nvlink_switch_bandwidth_sim(tensor_size_bytes: int, bus_bandwidth_gbps: float, bus_efficiency: float = 0.85) -> float:
    effective_bw = (bus_bandwidth_gbps * 1e9 / 8.0) * bus_efficiency
    if effective_bw <= 0:
        return 0.0
    ms = (tensor_size_bytes / effective_bw) * 1000.0
    return round(ms, 4)
