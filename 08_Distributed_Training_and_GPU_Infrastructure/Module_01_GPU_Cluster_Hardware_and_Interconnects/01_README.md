# Module 01: GPU Cluster Hardware & Interconnect Topologies

> **Architectural Scope**: NVLink 4.0, NVSwitch (900 GB/s), InfiniBand NDR (400 Gbps), RoCE v2, Rail-Optimized Network Fabrics, Fat-Tree vs Dragonfly, and Bisection Bandwidth.

---

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **5** | **[03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **6** | **[02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **7** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **8** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

## 1. The Physical Hierarchy of Modern AI Supercomputers

Modern foundation model training infrastructure is organized hierarchically into compute, node, rack, and cluster fabric layers:

```mermaid
flowchart TD
    subgraph Spine["Datacenter Spine Switch Fabric Layer"]
        Spine1["Spine Switch Core Aggregation"]
    end

    subgraph Leaf["Leaf Switch Layer (Rail-Optimized)"]
        Leaf0["Leaf Switch (Rack 0 / Rail 0)"]
        Leaf1["Leaf Switch (Rack 1 / Rail 1)"]
        LeafN["Leaf Switch (Rack N / Rail 7)"]
    end

    Spine1 --- Leaf0
    Spine1 --- Leaf1
    Spine1 --- LeafN

    subgraph Node["Server Node (e.g. DGX H100 with 8x H100 SXM5)"]
        direction TB
        subgraph NVLinkMesh["NVLink 4.0 High-Speed Mesh (900 GB/s per GPU Bi-dir)"]
            GPU0["GPU 0 (H100)"] <-->|900 GB/s| GPU1["GPU 1 (H100)"]
            GPU1 <-->|900 GB/s| GPUN["... GPU 7 (H100)"]
        end
        subgraph HCAs["Rail-Optimized HCAs (400 Gbps InfiniBand NDR)"]
            HCA0["HCA 0 (400 Gbps)"]
            HCA7["HCA 7 (400 Gbps)"]
        end
        GPU0 --- HCA0
        GPUN --- HCA7
    end

    HCA0 -->|InfiniBand NDR Optical Link| Leaf0
    HCA7 -->|InfiniBand NDR Optical Link| LeafN
```

### Physical Specifications Matrix
| Interconnect | Physical Media | Bandwidth per GPU | Latency | Scope |
| :--- | :--- | :---: | :---: | :--- |
| **NVLink 4.0 / NVSwitch** | On-board copper traces | $900 \text{ GB/s}$ bi-dir | $\approx 100 \text{ ns}$ | Intra-node (8 GPUs) |
| **PCIe Gen 5** | Motherboard PCIe lanes | $64 \text{ GB/s}$ bi-dir | $\approx 500 \text{ ns}$ | Host CPU to GPU |
| **InfiniBand NDR** | Optical / DAC cables | $400 \text{ Gbps (50 GB/s)}$ | $\approx 1.5 \; \mu\text{s}$ | Inter-node cluster |
| **RoCE v2 Ethernet** | 400GbE / 800GbE fiber | $50 - 100 \text{ GB/s}$ | $\approx 2.5 \; \mu\text{s}$ | Inter-node cluster |

---

## 2. Bisection Bandwidth & Fat-Tree Network Topology

In large clusters (1,024 to 24,000 GPUs), network switches are arranged in a **Fat-Tree topology** (Clos network):
- Leaf switches connect to compute nodes.
- Spine switches aggregate leaf switches.
- **1:1 Non-Blocking Guarantee**: The aggregate uplink bandwidth from all leaf switches to the spine equals the downlink bandwidth to the nodes.
- Bisection Bandwidth:
  $$\text{BW}_{\text{bisection}} = \frac{\text{Total Nodes}}{2} \times \text{Uplink Bandwidth per Node}$$

---

## 3. Module Study Progression
1. **Beginner Playground**: Read [00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md).
2. **Architecture Theory**: Study this [01_README.md](01_README.md).
3. **Hands-on Project**: Follow [02_PROJECT_GUIDE.md](02_PROJECT_GUIDE.md).
4. **Staff Interview Challenges**: Check [03_SELF_ASSESSMENT_AND_CHALLENGES.md](03_SELF_ASSESSMENT_AND_CHALLENGES.md).
5. **Production Debugging**: Review [04_TROUBLESHOOTING_AND_EDGE_CASES.md](04_TROUBLESHOOTING_AND_EDGE_CASES.md).
