# 🐣 Interactive Foundations Playground: GPU Cluster Hardware & Interconnects

> *"Inside a node GPUs talk over lightning-fast NVLink; across nodes they speak over InfiniBand networks."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Intra-Node NVLink vs Inter-Node Network

NVLink offers 900 GB/s bidirectional bandwidth per GPU; 400 Gbps InfiniBand delivers ~50 GB/s cross-node.

```python
nvlink_bw_gb_s = 900.0
ib_400g_gb_s = 50.0  # 400 Gbps = 50 GB/s
bandwidth_ratio = nvlink_bw_gb_s / ib_400g_gb_s

assert bandwidth_ratio == 18.0
print(f"NVLink is {bandwidth_ratio:.0f}x faster than 400 Gbps cross-node InfiniBand.")
```

---

## 2. PCIe vs NVLink Bus Saturation

PCIe Gen 5 provides 64 GB/s per x16 slot; NVLink eliminates host PCIe CPU bounce buffers.

```python
pcie_gen5_bw = 64.0
assert nvlink_bw_gb_s > pcie_gen5_bw
assert nvlink_bw_gb_s / pcie_gen5_bw > 10.0
print("NVLink provides over 10x headroom over standard PCIe Gen 5.")
```

---

## 3. Cluster Topology Bisection Bandwidth

In a fat-tree non-blocking spine-leaf network, bisection bandwidth equals the sum of all spine uplink capacities.

```python
num_leaf_switches = 8
uplinks_per_leaf = 4
uplink_bw_gb_s = 50.0
bisection_bw = (num_leaf_switches * uplinks_per_leaf * uplink_bw_gb_s) / 2

assert bisection_bw == 800.0
print(f"Cluster non-blocking bisection bandwidth: {bisection_bw} GB/s")
```

---
