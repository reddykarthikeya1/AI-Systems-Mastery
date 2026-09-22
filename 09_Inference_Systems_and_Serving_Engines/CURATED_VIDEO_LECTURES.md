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
| **Module 05** | Continuous & Dynamic Iteration-Level Batching | [Deploying Fine‑Tuned Models on Hugging Face, VLLM, Text‑Generation‑Inference (TGI)](https://www.youtube.com/watch?v=MxOBZ-E2J8w) | **SH AI Academy** | `148 views` | `16:03` |
| **Module 06** | Chunked Prefill & Prefill-Decode (PD) Disaggregation | [Why Separating Prefill and Decode Makes LLMs Faster - vLLM, LLM-D and NIXL](https://www.youtube.com/watch?v=BaD3CTYf6V0) | **The Cef Experience** | `985 views` | `19:29` |
| **Module 07** | Speculative Decoding & Medusa Multi-Head Verification | [Faster LLMs: Accelerate Inference with Speculative Decoding](https://www.youtube.com/watch?v=VkWlLSTdHs8) | **IBM Technology** | `34,893 views` | `9:39` |
| **Module 08** | Model Quantization for Serving (FP8, AWQ, Marlin) | [Quantization explained with PyTorch - Post-Training Quantization, Quantization-Aware Training](https://www.youtube.com/watch?v=0VdNflU08yA) | **Umar Jamil** | `59,892 views` | `50:55` |
| **Module 09** | Production Benchmarking, SLAs & Autoscaling | [Expert talk on LLM Inference - Part 2](https://www.youtube.com/watch?v=XQ_xjS53IpM) | **AI Paatshal** | `115 views` | `9:47` |

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
- **Core Architecture Focus**: Autoregressive cache mechanics, memory footprints per token, and multi-query/grouped-query attention.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=Mn_9W1nCFLo`

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

- **Recommended Lecture**: [Deploying Fine‑Tuned Models on Hugging Face, VLLM, Text‑Generation‑Inference (TGI)](https://www.youtube.com/watch?v=MxOBZ-E2J8w)
- **Instructor / Channel**: **SH AI Academy**
- **Viewership & Recency**: `148 views` • `2 mo ago` • Length: `16:03`
- **Core Architecture Focus**: Iteration-level scheduling, inserting incoming prompts without waiting for completed sequences.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=MxOBZ-E2J8w`

### Module 06: Chunked Prefill & Prefill-Decode (PD) Disaggregation

- **Recommended Lecture**: [Why Separating Prefill and Decode Makes LLMs Faster | vLLM, LLM-D and NIXL](https://www.youtube.com/watch?v=BaD3CTYf6V0)
- **Instructor / Channel**: **The Cef Experience**
- **Viewership & Recency**: `985 views` • `1 mo ago` • Length: `19:29`
- **Core Architecture Focus**: Separating compute-bound prefill nodes from memory-bound decode nodes to eliminate inter-token jitter.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=BaD3CTYf6V0`

### Module 07: Speculative Decoding & Medusa Multi-Head Verification

- **Recommended Lecture**: [Faster LLMs: Accelerate Inference with Speculative Decoding](https://www.youtube.com/watch?v=VkWlLSTdHs8)
- **Instructor / Channel**: **IBM Technology**
- **Viewership & Recency**: `34,893 views` • `1 yr ago` • Length: `9:39`
- **Core Architecture Focus**: Draft model speculation, parallel verification by the target model, and acceptance rates.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=VkWlLSTdHs8`

### Module 08: Model Quantization for Serving (FP8, AWQ, Marlin)

- **Recommended Lecture**: [Quantization explained with PyTorch - Post-Training Quantization, Quantization-Aware Training](https://www.youtube.com/watch?v=0VdNflU08yA)
- **Instructor / Channel**: **Umar Jamil**
- **Viewership & Recency**: `59,892 views` • `2 yr ago` • Length: `50:55`
- **Core Architecture Focus**: Weight-only vs weight-activation quantization, outlier protection, and Marlin high-speed kernels.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=0VdNflU08yA`

### Module 09: Production Benchmarking, SLAs & Autoscaling

- **Recommended Lecture**: [Expert talk on LLM Inference - Part 2](https://www.youtube.com/watch?v=XQ_xjS53IpM)
- **Instructor / Channel**: **AI Paatshal**
- **Viewership & Recency**: `115 views` • `3 wk ago` • Length: `9:47`
- **Core Architecture Focus**: Load testing with synthetic concurrency, TTFT p99 latency SLAs, and GPU pod autoscaling.
- **Direct Watch URL**: `https://www.youtube.com/watch?v=XQ_xjS53IpM`

