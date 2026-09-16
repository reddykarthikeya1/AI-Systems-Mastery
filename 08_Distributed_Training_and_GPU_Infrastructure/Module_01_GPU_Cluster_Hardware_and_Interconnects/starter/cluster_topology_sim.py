"""Starter template for GPU Cluster Topology Simulator."""
from __future__ import annotations


def calculate_bisection_bandwidth(
    num_nodes: int,
    gpus_per_node: int = 8,
    nic_bandwidth_gbs: float = 50.0,
    oversubscription_ratio: float = 1.0,
) -> float:
    """Calculate cluster bisection bandwidth in GB/s."""
    raise NotImplementedError("Implement calculate_bisection_bandwidth")


def estimate_transfer_time(
    src_gpu: tuple[int, int],
    dst_gpu: tuple[int, int],
    size_bytes: int,
    nvlink_bw_gbs: float = 900.0,
    ib_bw_gbs: float = 50.0,
    nvlink_latency_us: float = 0.2,
    ib_latency_us: float = 1.5,
) -> float:
    """Estimate point-to-point transfer time in microseconds."""
    raise NotImplementedError("Implement estimate_transfer_time")


def check_rail_alignment(src_gpu_idx: int, dst_gpu_idx: int) -> bool:
    """Check if two GPUs are on the same rail (same local GPU index)."""
    raise NotImplementedError("Implement check_rail_alignment")
