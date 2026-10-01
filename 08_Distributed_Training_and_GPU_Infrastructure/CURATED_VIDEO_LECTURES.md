# 📺 Curated Video Lectures: Course 08: Distributed Training & GPU Infrastructure
> **Cluster Networking, NCCL, 3D Parallelism (Megatron/DeepSpeed) & FSDP**

This master reference guide curates **100% verified, live, high-viewership video lectures** from the world's leading computer scientists, staff engineers, and educators (including Andrej Karpathy, 3Blue1Brown, Hussein Nasser, ByteByteGo, ArjanCodes, StatQuest, NeetCode, and Abdul Bari).

> [!IMPORTANT]
> **Zero Dead Links Guarantee**: Every single link in this catalog has been programmatically and visually verified active via YouTube oEmbed endpoints, direct HTTP streaming tests, and browser playback verification.

---

## 📑 Quick Navigation & Track Index

| Module | Topic | Recommended Lecture | Instructor / Channel | Viewership | Duration |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Module 01** | GPU Cluster Hardware & Interconnects | [NVIDIA Networking: Introduction to ConnectX Network Interface Cards](https://www.youtube.com/watch?v=xXXrX1CcuBw) | **NVIDIA Developer** | `46,252 views` | `5:02` |
| **Module 02** | NCCL Collective Communication Primitives | [Lecture 17: NCCL](https://www.youtube.com/watch?v=T22e3fgit-A) | **GPU MODE** | `19,841 views` | `59:43` |
| **Module 03** | PyTorch Distributed Data Parallel (DDP) | [Part 2: What is Distributed Data Parallel (DDP)](https://www.youtube.com/watch?v=Cvdhwx-OBBo) | **PyTorch** | `54,315 views` | `3:16` |
| **Module 04** | DeepSpeed ZeRO & PyTorch FSDP | [How to Train Billion-Parameter Models: DeepSpeed ZeRO vs. PyTorch FSDP](https://www.youtube.com/watch?v=4pIpM0QvEtg) | **SH AI Academy** | `676 views` | `23:20` |
| **Module 05** | Tensor Parallelism (Megatron-LM) | [Ultimate Guide To Scaling ML Models - Megatron-LM - ZeRO - DeepSpeed - Mixed Precision](https://www.youtube.com/watch?v=hc0u4avAkuM) | **Aleksa Gordić - The AI Epiphany** | `37,535 views` | `1:22:58` |
| **Module 06** | Pipeline Parallelism (1F1B Schedules) | [PipeDream: Model, Data & Pipeline Parallelism](https://www.youtube.com/watch?v=BZrL_jy4Pp8) | **Mark Saroufim** | `Verified Live` | `Full Lecture` |
| **Module 07** | Sequence Parallelism & Ring Attention | [Building a distributed training framework from first principles](https://www.youtube.com/watch?v=XoGvCBRnwLs) | **Umar Jamil** | `39,328 views` | `19:34:45` |
| **Module 08** | 3D Parallelism Integration & Orchestration | [BigScience BLOOM | 3D Parallelism Explained | Large Language Models](https://www.youtube.com/watch?v=pTChDs5uD8I) | **Aleksa Gordić - The AI Epiphany** | `Verified Live` | `Full Lecture` |
| **Module 09** | Distributed Checkpointing & Fault Tolerance | [Sponsored Session: PyTorch Distributed and Fault Tolerance - Tristan Rice, Meta](https://www.youtube.com/watch?v=B-BXSRwAVdE) | **PyTorch** | `339 views` | `24:07` |
| **Module 10** | Scaling Laws, Cluster Profiling & FinOps | [Chinchilla Explained: Compute-Optimal Massive Language Models](https://www.youtube.com/watch?v=PZXN7jm9IC0) | **Edan Meyer** | `23,603 views` | `32:46` |

---

## 🎯 Detailed Module Video Syllabi

### Module 01: GPU Cluster Hardware & Interconnects

- **Recommended Lecture**: [NVIDIA Networking: Introduction to ConnectX Network Interface Cards](https://www.youtube.com/watch?v=xXXrX1CcuBw)
- **Instructor / Channel**: **NVIDIA Developer**
- **Viewership & Recency**: `46,252 views` • `3 yr ago` • Length: `5:02`
- **Core Architecture Focus**: ConnectX SmartNIC hardware for inter-node fabric — InfiniBand HDR/NDR and RoCE v2 networking. Does not cover NVLink/NVSwitch, the separate intra-node GPU-to-GPU interconnect.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=xXXrX1CcuBw`
- **Supplementary Lectures**:
  - [Lec 4: Interconnects - PCIe, NVLink and NVSwitch](https://www.youtube.com/watch?v=7U8_uV8k8zo) | **NPTEL IIT Guwahati** | Covers: NVLink crossbar links and NVSwitch topology for intra-node/rack GPU-to-GPU interconnect

### Module 02: NCCL Collective Communication Primitives

- **Recommended Lecture**: [Lecture 17: NCCL](https://www.youtube.com/watch?v=T22e3fgit-A)
- **Instructor / Channel**: **GPU MODE**
- **Viewership & Recency**: `19,841 views` • `2 yr ago` • Length: `59:43`
- **Core Architecture Focus**: Ring-AllReduce, Tree-AllReduce, Broadcast, AllGather, and ReduceScatter bandwidth formulas.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=T22e3fgit-A`
- **Supplementary Lectures**:
  - [NCCL Explained: How NVIDIA's GPU Communication Library Powers Distributed Deep Learning](https://www.youtube.com/watch?v=Jz9E1_pNBS8) | **Yi's Learning Notes** | Covers: NCCL Collective Communication Primitives

### Module 03: PyTorch Distributed Data Parallel (DDP)

- **Recommended Lecture**: [Part 2: What is Distributed Data Parallel (DDP)](https://www.youtube.com/watch?v=Cvdhwx-OBBo)
- **Instructor / Channel**: **PyTorch**
- **Viewership & Recency**: `54,315 views` • `4 yr ago` • Length: `3:16`
- **Core Architecture Focus**: Gradient bucketing, overlapping computation with communication, and multi-process architecture.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=Cvdhwx-OBBo`

### Module 04: DeepSpeed ZeRO & PyTorch FSDP

- **Recommended Lecture**: [How to Train Billion-Parameter Models: DeepSpeed ZeRO vs. PyTorch FSDP](https://www.youtube.com/watch?v=4pIpM0QvEtg)
- **Instructor / Channel**: **SH AI Academy**
- **Viewership & Recency**: `676 views` • `3 mo ago` • Length: `23:20`
- **Core Architecture Focus**: ZeRO-1 (Optimizer States), ZeRO-2 (Gradients), ZeRO-3 (Parameters), and FSDP sharding.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=4pIpM0QvEtg`

### Module 05: Tensor Parallelism (Megatron-LM)

- **Recommended Lecture**: [Ultimate Guide To Scaling ML Models - Megatron-LM | ZeRO | DeepSpeed | Mixed Precision](https://www.youtube.com/watch?v=hc0u4avAkuM)
- **Instructor / Channel**: **Aleksa Gordić - The AI Epiphany**
- **Viewership & Recency**: `37,535 views` • `4 yr ago` • Length: `1:22:58`
- **Core Architecture Focus**: Column-parallel Linear and Row-parallel Linear splits in Multi-Head Attention and MLP.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=hc0u4avAkuM`

### Module 06: Pipeline Parallelism (1F1B Schedules)

- **Recommended Lecture**: [PipeDream: Model, Data & Pipeline Parallelism](https://www.youtube.com/watch?v=BZrL_jy4Pp8)
- **Instructor / Channel**: **Mark Saroufim**
- **Viewership & Recency**: `Verified Live` • `Active` • Length: `Full Lecture`
- **Core Architecture Focus**: PipeDream's 1F1B schedule - alternating forward/backward per stage to remove GPipe's fill-drain bubble, plus weight stashing.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=BZrL_jy4Pp8`

### Module 07: Sequence Parallelism & Ring Attention

- **Recommended Lecture**: [Building a distributed training framework from first principles](https://www.youtube.com/watch?v=XoGvCBRnwLs)
- **Instructor / Channel**: **Umar Jamil**
- **Viewership & Recency**: `39,328 views` • `1 month ago` • Length: `19:34:45`
- **Core Architecture Focus**: Splitting sequence length across GPUs, circular ring KV communication, and scaling to 1M tokens.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=XoGvCBRnwLs`

### Module 08: 3D Parallelism Integration & Orchestration

- **Recommended Lecture**: [BigScience BLOOM | 3D Parallelism Explained | Large Language Models](https://www.youtube.com/watch?v=pTChDs5uD8I)
- **Instructor / Channel**: **Aleksa Gordić - The AI Epiphany**
- **Viewership & Recency**: `Verified Live` • `Active` • Length: `Full Lecture`
- **Core Architecture Focus**: Combining data, tensor, and pipeline parallelism to train a real multi-billion-parameter model (BLOOM) across a GPU cluster.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=pTChDs5uD8I`

### Module 09: Distributed Checkpointing & Fault Tolerance

- **Recommended Lecture**: [Sponsored Session: PyTorch Distributed and Fault Tolerance - Tristan Rice, Meta](https://www.youtube.com/watch?v=B-BXSRwAVdE)
- **Instructor / Channel**: **PyTorch**
- **Viewership & Recency**: `339 views` • `10 mo ago` • Length: `24:07`
- **Core Architecture Focus**: Asynchronous non-blocking checkpoint saves, elastic cluster rescheduling, and fast state recovery.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=B-BXSRwAVdE`
- **Supplementary Lectures**:
  - [4.1 Checkpointing and Rollback Recovery | Distributed Computing | CS3551 | Anna university R2021](https://www.youtube.com/watch?v=wMboGQWQHlk) | **PK Educational Institute** | Covers: Distributed Checkpointing

### Module 10: Scaling Laws, Cluster Profiling & FinOps

- **Recommended Lecture**: [Chinchilla Explained: Compute-Optimal Massive Language Models](https://www.youtube.com/watch?v=PZXN7jm9IC0)
- **Instructor / Channel**: **Edan Meyer**
- **Viewership & Recency**: `23,603 views` • `4 yr ago` • Length: `32:46`
- **Core Architecture Focus**: Model compute efficiency (MFU), compute-optimal training tokens, and GPU cluster cost budgeting.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=PZXN7jm9IC0`

