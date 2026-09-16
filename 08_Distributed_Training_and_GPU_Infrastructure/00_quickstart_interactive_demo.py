"""Course 08 Quickstart: Interactive Distributed Training & Interconnect Topology Demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Module_01_GPU_Cluster_Hardware_and_Interconnects" / "project_solution"))
from interconnect_topology_sim import ClusterTopologySimulator


def run_demo() -> None:
    print("=" * 70)
    print(" COURSE 08: DISTRIBUTED TRAINING & GPU INFRASTRUCTURE QUICKSTART")
    print("=" * 70)

    print("\n[1] Physical Cluster Interconnect Latency & Bandwidth Benchmark:")
    tensor_sizes = [50 * 1024 * 1024, 250 * 1024 * 1024, 1024 * 1024 * 1024]
    tiers = ["nvlink4", "pcie_gen5", "infiniband_ndr"]

    for size in tensor_sizes:
        size_mb = size / (1024 * 1024)
        print(f"\n  -- Ring All-Reduce for {size_mb:.0f} MB Gradient Tensor (World Size = 8 GPUs) --")
        for tier in tiers:
            time_ms = ClusterTopologySimulator.calculate_ring_allreduce_time(size, world_size=8, tier=tier) * 1000
            name = ClusterTopologySimulator.TIERS[tier].name
            bw = ClusterTopologySimulator.TIERS[tier].bandwidth_gb_per_sec
            print(f"     * {name:<26} (BW: {bw:>5.0f} GB/s) -> All-Reduce Time: {time_ms:>6.2f} ms")

    print("\n[2] Computation-Communication Overlap Efficiency:")
    cases = [(0.015, 0.010), (0.010, 0.015), (0.005, 0.020)]
    for compute, comm in cases:
        eff = ClusterTopologySimulator.compute_overlap_efficiency(compute, comm) * 100
        print(f"     * Compute: {compute*1000:>4.1f}ms | Comm: {comm*1000:>4.1f}ms -> Hidden Overlap: {eff:>5.1f}%")

    print("\n" + "=" * 70)
    print(" QUICKSTART DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
