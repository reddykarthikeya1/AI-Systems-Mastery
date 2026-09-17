"""Beginner playground for Module 01 - GPU Cluster Hardware & Interconnects.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Intra-Node NVLink vs Inter-Node Network
nvlink_bw_gb_s = 900.0
ib_400g_gb_s = 50.0  # 400 Gbps = 50 GB/s
bandwidth_ratio = nvlink_bw_gb_s / ib_400g_gb_s

assert bandwidth_ratio == 18.0
print(f"NVLink is {bandwidth_ratio:.0f}x faster than 400 Gbps cross-node InfiniBand.")

# -------------------------------------------- 2. PCIe vs NVLink Bus Saturation
pcie_gen5_bw = 64.0
assert nvlink_bw_gb_s > pcie_gen5_bw
assert nvlink_bw_gb_s / pcie_gen5_bw > 10.0
print("NVLink provides over 10x headroom over standard PCIe Gen 5.")

# -------------------------------------------- 3. Cluster Topology Bisection Bandwidth
num_leaf_switches = 8
uplinks_per_leaf = 4
uplink_bw_gb_s = 50.0
bisection_bw = (num_leaf_switches * uplinks_per_leaf * uplink_bw_gb_s) / 2

assert bisection_bw == 800.0
print(f"Cluster non-blocking bisection bandwidth: {bisection_bw} GB/s")

print()
print("All checks passed.")
