"""Production reference implementation for GPU Cluster Topology Simulator."""
from __future__ import annotations


def calculate_bisection_bandwidth(
    num_nodes: int,
    gpus_per_node: int = 8,
    nic_bandwidth_gbs: float = 50.0,
    oversubscription_ratio: float = 1.0,
) -> float:
    """Calculate cluster bisection bandwidth in GB/s.

    Bisection bandwidth cuts the cluster in half.
    Total cross-sectional links = (num_nodes / 2) * gpus_per_node * nic_bandwidth / oversubscription.
    """
    if num_nodes < 2 or oversubscription_ratio <= 0:
        raise ValueError("Must have at least 2 nodes and positive oversubscription ratio.")

    nodes_per_half = num_nodes / 2.0
    uplink_per_half = nodes_per_half * gpus_per_node * nic_bandwidth_gbs
    bisection_bw = uplink_per_half / oversubscription_ratio
    return bisection_bw


def estimate_transfer_time(
    src_gpu: tuple[int, int],
    dst_gpu: tuple[int, int],
    size_bytes: int,
    nvlink_bw_gbs: float = 900.0,
    ib_bw_gbs: float = 50.0,
    nvlink_latency_us: float = 0.2,
    ib_latency_us: float = 1.5,
) -> float:
    """Estimate point-to-point transfer time in microseconds.

    src_gpu: (node_id, local_gpu_id)
    dst_gpu: (node_id, local_gpu_id)
    """
    if size_bytes <= 0:
        return 0.0

    src_node, _ = src_gpu
    dst_node, _ = dst_gpu

    size_gb = size_bytes / (1024.0 ** 3)

    if src_node == dst_node:
        # Intra-node NVLink transfer
        transfer_us = (size_gb / nvlink_bw_gbs) * 1e6
        total_time_us = nvlink_latency_us + transfer_us
    else:
        # Inter-node transfer over InfiniBand
        transfer_us = (size_gb / ib_bw_gbs) * 1e6
        # Crossing node requires NVLink egress + IB network + NVLink ingress
        total_time_us = (2 * nvlink_latency_us + ib_latency_us) + transfer_us

    return total_time_us


def check_rail_alignment(src_gpu_idx: int, dst_gpu_idx: int) -> bool:
    """Check if two GPUs are on the same rail (same local GPU index).

    In rail-optimized clusters, GPU i in any node connects directly to Rail i switch,
    avoiding inter-rail crossbar contention.
    """
    return src_gpu_idx == dst_gpu_idx
