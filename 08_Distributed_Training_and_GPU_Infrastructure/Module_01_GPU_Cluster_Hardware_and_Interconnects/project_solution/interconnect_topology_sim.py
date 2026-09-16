"""Hardware Interconnect Topology and NCCL Ring All-Reduce Latency Simulator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InterconnectTier:
    name: str
    bandwidth_gb_per_sec: float
    base_latency_us: float


class ClusterTopologySimulator:
    """Simulates multi-tier GPU cluster communication latencies (NVLink vs InfiniBand)."""

    TIERS = {
        "nvlink4": InterconnectTier("NVLink 4 / NVSwitch", bandwidth_gb_per_sec=900.0, base_latency_us=0.5),
        "pcie_gen5": InterconnectTier("PCIe Gen5 x16", bandwidth_gb_per_sec=64.0, base_latency_us=2.5),
        "infiniband_ndr": InterconnectTier("InfiniBand NDR 400G", bandwidth_gb_per_sec=50.0, base_latency_us=1.8),
    }

    @classmethod
    def calculate_ring_allreduce_time(
        cls,
        tensor_size_bytes: int,
        world_size: int,
        tier: str = "nvlink4",
    ) -> float:
        """Calculates All-Reduce time using standard ring model:
        T = 2 * ((N - 1) / N) * (S / B) + 2 * (N - 1) * alpha
        """
        interconnect = cls.TIERS.get(tier, cls.TIERS["nvlink4"])
        n = world_size
        s_gb = tensor_size_bytes / 1e9

        bw_time_sec = 2.0 * ((n - 1) / n) * (s_gb / interconnect.bandwidth_gb_per_sec)
        latency_sec = 2.0 * (n - 1) * (interconnect.base_latency_us * 1e-6)
        return bw_time_sec + latency_sec

    @classmethod
    def compute_overlap_efficiency(
        cls,
        compute_time_sec: float,
        comm_time_sec: float,
    ) -> float:
        """Calculates communication-computation overlap ratio (1.0 = perfect hiding)."""
        if compute_time_sec <= 0:
            return 0.0
        hidden_comm = min(compute_time_sec, comm_time_sec)
        return hidden_comm / comm_time_sec if comm_time_sec > 0 else 1.0
