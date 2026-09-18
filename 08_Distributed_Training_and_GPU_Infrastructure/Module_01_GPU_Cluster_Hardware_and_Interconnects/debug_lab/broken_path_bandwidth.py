# Debug Lab: Multi-Hop Interconnect Bandwidth Estimator Reports the Wrong Link's Speed
# Course 08 - Module 01 GPU Cluster Hardware and Interconnects

LINK_BW_GBPS = {
    ("gpu0", "gpu1"): 900,    # intra-node NVLink
    ("gpu1", "nic0"): 400,    # PCIe Gen5 to the NIC
    ("nic0", "nic1"): 200,    # inter-node InfiniBand (HDR)
    ("nic1", "gpu2"): 400,    # PCIe Gen5 from the NIC
}


def hop_bandwidth(a, b):
    return LINK_BW_GBPS.get((a, b)) or LINK_BW_GBPS.get((b, a))


def path_bandwidth(path):
    hops = list(zip(path, path[1:]))
    hop_speeds = [hop_bandwidth(a, b) for a, b in hops]
    return max(hop_speeds), hop_speeds


def transfer_eta_seconds(payload_gb, path):
    effective_bw, _ = path_bandwidth(path)
    return payload_gb / effective_bw


if __name__ == "__main__":
    path = ["gpu0", "gpu1", "nic0", "nic1", "gpu2"]  # cross-node, one GPU per node
    payload_gb = 100

    effective_bw, hop_speeds = path_bandwidth(path)
    bottleneck_bw = min(hop_speeds)
    eta = transfer_eta_seconds(payload_gb, path)
    true_eta = payload_gb / bottleneck_bw

    print(f"Path: {' -> '.join(path)}")
    print(f"Per-hop bandwidths (GB/s): {hop_speeds}")
    print(f"Estimator's effective path bandwidth: {effective_bw} GB/s -> ETA for {payload_gb} GB: {eta:.4f} s")
    print(f"True bottleneck-hop bandwidth:         {bottleneck_bw} GB/s -> ETA for {payload_gb} GB: {true_eta:.4f} s")
