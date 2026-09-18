# Debug Lab Incident Report: Cross-Node Transfer ETA Estimator Ignores the Slowest Hop

- **Severity:** P1 Capacity Planning Error
- **Affected Subsystem:** Module_01_GPU_Cluster_Hardware_and_Interconnects
- **Reported Impact:** A path-bandwidth estimator walks a 4-hop route from `gpu0` on one node, across NVLink and PCIe, over the inter-node InfiniBand link, to `gpu2` on a second node, and reports an "effective path bandwidth" used to compute a transfer ETA. The reported bandwidth is far higher than the slowest link on the route, and the resulting ETA is a large underestimate.

---

## 🚨 Observable Symptoms & Logs
```text
Path: gpu0 -> gpu1 -> nic0 -> nic1 -> gpu2
Per-hop bandwidths (GB/s): [900, 400, 200, 400]
Estimator's effective path bandwidth: 900 GB/s -> ETA for 100 GB: 0.1111 s
True bottleneck-hop bandwidth:         200 GB/s -> ETA for 100 GB: 0.5000 s
```
Data moving along this path must physically pass through all four hops in sequence, including the 200 GB/s inter-node InfiniBand hop. The estimator reports 900 GB/s -- the fastest single hop on the entire route (intra-node NVLink) -- as if that were the speed of the whole transfer, producing an ETA more than 4x too optimistic.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_GPU_Cluster_Hardware_and_Interconnects/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_path_bandwidth.py
   ```
3. Compare the "Estimator's effective path bandwidth" line against the "True bottleneck-hop bandwidth" line and their respective ETAs.

---

## 🎯 Your Objective
1. Inspect `broken_path_bandwidth.py`'s `path_bandwidth()` function and how it combines the four `hop_speeds` values into a single "effective" bandwidth.
2. Work out how a multi-hop, strictly-serial data path's end-to-end throughput actually relates to its individual hops' bandwidths.
3. Formulate a hypothesis for why picking out the fastest hop instead of the slowest one produces an overly optimistic estimate, then check `ANSWERS.md`.
