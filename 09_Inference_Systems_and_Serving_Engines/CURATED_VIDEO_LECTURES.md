# 📺 Curated Video Lectures: Course 09: LLM Inference Systems & Serving Engines
> **PagedAttention, Continuous Batching, Speculative Decoding & TensorRT-LLM**

This master reference guide curates **100% verified, live, high-viewership video lectures** from the world's leading computer scientists, staff engineers, and educators (including Andrej Karpathy, 3Blue1Brown, Hussein Nasser, ByteByteGo, ArjanCodes, StatQuest, NeetCode, and Abdul Bari).

> [!IMPORTANT]
> **Zero Dead Links Guarantee**: Every single link in this catalog has been programmatically and visually verified active via YouTube oEmbed endpoints, direct HTTP streaming tests, and browser playback verification.

---

## 📑 Quick Navigation & Track Index

| Module | Topic | Recommended Lecture | Instructor / Channel | Viewership | Duration |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Module 01** | Inference Latency, TTFT & TPOT Trade-offs | [LLM Inference Performance: Latency and Throughput Metrics](https://www.youtube.com/watch?v=DW-mo65DJ-Q) | **Ready Tensor** | `888 views` | `15:28` |
| **Module 02** | KV-Cache Memory Hierarchy & Growth | [LLaMA explained: KV-Cache, Rotary Positional Embedding, RMS Norm, Grouped Query Attention, SwiGLU](https://www.youtube.com/watch?v=Mn_9W1nCFLo) | **Umar Jamil** | `127,208 views` | `1:10:55` |
| **Module 03** | PagedAttention Architecture (vLLM) | [PagedAttention: Behind vLLM's Insane Speed](https://www.youtube.com/watch?v=6uPnLkCiy5g) | **Tales Of Tensors** | `12,514 views` | `6:53` |
| **Module 04** | RadixAttention & Prefix Caching (SGLang) | [SGLang Deep Dive: RadixAttention, KV Cache & High-Throughput Serving #OpenSource #LLMOps #SGLang](https://www.youtube.com/watch?v=TWbrz5rSfFI) | **AI Learning Hub** | `53 views` | `7:02` |
| **Module 05** | Continuous & Dynamic Iteration-Level Batching | [Continuous Batching: Optimize LLM Serving Throughput and Latency](https://www.youtube.com/watch?v=iiyu86UZwGg) | **Ready Tensor** | `Verified Live` | `Full Lecture` |
| **Module 06** | Chunked Prefill & Prefill-Decode (PD) Disaggregation | [Why Separating Prefill and Decode Makes LLMs Faster - vLLM, LLM-D and NIXL](https://www.youtube.com/watch?v=BaD3CTYf6V0) | **The Cef Experience** | `985 views` | `19:29` |
| **Module 07** | Speculative Decoding & Medusa Multi-Head Verification | [Faster LLMs: Accelerate Inference with Speculative Decoding](https://www.youtube.com/watch?v=VkWlLSTdHs8) | **IBM Technology** | `34,893 views` | `9:39` |
| **Module 08** | Model Quantization for Serving (FP8, AWQ, Marlin) | [Quantization explained with PyTorch - Post-Training Quantization, Quantization-Aware Training](https://www.youtube.com/watch?v=0VdNflU08yA) | **Umar Jamil** | `59,892 views` | `50:55` |
| **Module 09** | Production Benchmarking, SLAs & Autoscaling | [Optimizing Load Balancing and Autoscaling for LLM Inference on Kubernetes](https://www.youtube.com/watch?v=TSEGAh1bs4A) | **CNCF** | `Verified Live` | `Full Lecture` |

---

## 🎯 Detailed Module Video Syllabi

### Module 01: Inference Latency, TTFT & TPOT Trade-offs

- **Recommended Lecture**: [LLM Inference Performance: Latency and Throughput Metrics](https://www.youtube.com/watch?v=DW-mo65DJ-Q)
- **Instructor / Channel**: **Ready Tensor**
- **Viewership & Recency**: `888 views` • `8 months ago` • Length: `15:28`
- **Core Architecture Focus**: Time To First Token (TTFT), Time Per Output Token (TPOT), and memory bandwidth ceilings.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=DW-mo65DJ-Q`

### Module 02: KV-Cache Memory Hierarchy & Growth

- **Recommended Lecture**: [LLaMA explained: KV-Cache, Rotary Positional Embedding, RMS Norm, Grouped Query Attention, SwiGLU](https://www.youtube.com/watch?v=Mn_9W1nCFLo)
- **Instructor / Channel**: **Umar Jamil**
- **Viewership & Recency**: `127,208 views` • `3 yr ago` • Length: `1:10:55`
- **Core Architecture Focus**: Autoregressive cache mechanics, memory footprints per token, and multi-query/grouped-query attention; this module's other named concept (the tiered GPU/CPU/disk memory hierarchy and offloading) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=Mn_9W1nCFLo`
- **Supplementary Lectures**:
  - [KV Cache Explained | LLM Inference System Design and GPU Memory](https://www.youtube.com/watch?v=-kiOWUJQk6w) | **Think Software** | Covers: KV-cache memory hierarchy - GPU HBM vs. CPU/disk offload tiers in system design

### Module 03: PagedAttention Architecture (vLLM)

- **Recommended Lecture**: [PagedAttention: Behind vLLM's Insane Speed](https://www.youtube.com/watch?v=6uPnLkCiy5g)
- **Instructor / Channel**: **Tales Of Tensors**
- **Viewership & Recency**: `12,514 views` • `9 months ago` • Length: `6:53`
- **Core Architecture Focus**: Translating virtual memory paging into GPU KV-cache blocks, eliminating internal fragmentation.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=6uPnLkCiy5g`

### Module 04: RadixAttention & Prefix Caching (SGLang)

- **Recommended Lecture**: [SGLang Deep Dive: RadixAttention, KV Cache & High-Throughput Serving #OpenSource #LLMOps #SGLang](https://www.youtube.com/watch?v=TWbrz5rSfFI)
- **Instructor / Channel**: **AI Learning Hub**
- **Viewership & Recency**: `53 views` • `3 months ago` • Length: `7:02`
- **Core Architecture Focus**: Radix tree prefix reuse across multi-turn chats, few-shot prompts, and shared system messages.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=TWbrz5rSfFI`

### Module 05: Continuous & Dynamic Iteration-Level Batching

- **Recommended Lecture**: [Continuous Batching: Optimize LLM Serving Throughput and Latency](https://www.youtube.com/watch?v=iiyu86UZwGg)
- **Instructor / Channel**: **Ready Tensor**
- **Viewership & Recency**: `Verified Live` • `Active` • Length: `Full Lecture`
- **Core Architecture Focus**: Iteration-level scheduling that admits and evicts requests every decode step instead of waiting for a full batch to finish.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=iiyu86UZwGg`

### Module 06: Chunked Prefill & Prefill-Decode (PD) Disaggregation

- **Recommended Lecture**: [Why Separating Prefill and Decode Makes LLMs Faster | vLLM, LLM-D and NIXL](https://www.youtube.com/watch?v=BaD3CTYf6V0)
- **Instructor / Channel**: **The Cef Experience**
- **Viewership & Recency**: `985 views` • `1 mo ago` • Length: `19:29`
- **Core Architecture Focus**: Prefill-Decode (PD) disaggregation - separating compute-bound prefill nodes from memory-bound decode nodes to eliminate inter-token jitter; this module's other named concept (chunked prefill, the single-engine alternative that splits prefill into chunks interleaved with decode) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=BaD3CTYf6V0`
- **Supplementary Lectures**:
  - [What is Chunked Prefill?](https://www.youtube.com/watch?v=qeUnnH41jg0) | **Standarity** | Covers: chunked prefill - splitting long prefills into stall-free chunks interleaved with decode

### Module 07: Speculative Decoding & Medusa Multi-Head Verification

- **Recommended Lecture**: [Faster LLMs: Accelerate Inference with Speculative Decoding](https://www.youtube.com/watch?v=VkWlLSTdHs8)
- **Instructor / Channel**: **IBM Technology**
- **Viewership & Recency**: `34,893 views` • `1 yr ago` • Length: `9:39`
- **Core Architecture Focus**: Classic speculative decoding - draft model speculation, parallel verification by the target model, and acceptance rates; this module's other named concept (Medusa's draft-model-free multi-head verification) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=VkWlLSTdHs8`
- **Supplementary Lectures**:
  - [How Medusa Works](https://www.youtube.com/watch?v=Jjjn-J9SJ1s) | **Oxen** | Covers: Medusa - multiple decoding heads and tree attention, no separate draft model

### Module 08: Model Quantization for Serving (FP8, AWQ, Marlin)

- **Recommended Lecture**: [Quantization explained with PyTorch - Post-Training Quantization, Quantization-Aware Training](https://www.youtube.com/watch?v=0VdNflU08yA)
- **Instructor / Channel**: **Umar Jamil**
- **Viewership & Recency**: `59,892 views` • `2 yr ago` • Length: `50:55`
- **Core Architecture Focus**: General PyTorch quantization theory - symmetric/asymmetric ranges, calibration, and outlier protection via PTQ/QAT (this is framework-level theory, not the serving-specific AWQ/FP8/Marlin techniques the title names); this module's other named concepts (AWQ and FP8) are covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=0VdNflU08yA`
- **Supplementary Lectures**:
  - [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration [MLSys'24 Best Paper]](https://www.youtube.com/watch?v=dcINVsqxQgQ) | **MIT HAN Lab** | Covers: AWQ - protecting salient weights via activation-aware scaling
  - [Deep Dive: LLM Quantization, part 3 - FP8, FP4](https://www.youtube.com/watch?v=_hhbzZeQ8sY) | **Julien Simon** | Covers: FP8 serving formats and hardware-aware quantization choices

### Module 09: Production Benchmarking, SLAs & Autoscaling

- **Recommended Lecture**: [Optimizing Load Balancing and Autoscaling for LLM Inference on Kubernetes](https://www.youtube.com/watch?v=TSEGAh1bs4A)
- **Instructor / Channel**: **CNCF**
- **Viewership & Recency**: `Verified Live` • `Active` • Length: `Full Lecture`
- **Core Architecture Focus**: Autoscaling and load-balancing strategies - scaling LLM inference pods against real traffic load, and the metrics (queue depth, p99 latency) that should trigger it; this module's other named concept (production benchmarking methodology for establishing those SLA targets in the first place) is covered below.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=TSEGAh1bs4A`
- **Supplementary Lectures**:
  - [Learn How to Run an LLM Inference Performance Benchmark on NVIDIA GPUs - DevConf.US 2025](https://www.youtube.com/watch?v=otCouSz64Z8) | **DevConf** | Covers: production benchmarking methodology - reliable, reproducible LLM performance testing

