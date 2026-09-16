# Master Syllabus: 09. AI Inference Systems & Serving Engines

> 9 Core Modules · Production Reference Simulators · Staff-Level Case Studies · 10/10 Masterclass

## Course Curriculum Matrix

| # | Module | Core Systems Covered | Hands-on Project Deliverable |
|---|---|---|---|
| **01** | [Inference Latency & Throughput Trade-offs](Module_01_Inference_Latency_Throughput_Tradeoffs/01_README.md) | TTFT vs TPOT, Compute-bound Prefill vs Memory-bound Decode, Roofline Analysis | [Inference Metrics Simulator](Module_01_Inference_Latency_Throughput_Tradeoffs/02_PROJECT_GUIDE.md) |
| **02** | [KV-Cache Memory Management](Module_02_KV_Cache_Memory_Management/01_README.md) | Memory footprint formulas, MHA vs GQA vs MQA, Internal/External Fragmentation | [KV Cache Allocator](Module_02_KV_Cache_Memory_Management/02_PROJECT_GUIDE.md) |
| **03** | [PagedAttention Architecture (vLLM)](Module_03_PagedAttention_Architecture_vLLM/01_README.md) | Block tables, Physical block manager, Copy-on-Write parallel sampling | [PagedAttention Block Manager](Module_03_PagedAttention_Architecture_vLLM/02_PROJECT_GUIDE.md) |
| **04** | [RadixAttention & Prefix Caching](Module_04_RadixAttention_and_Prefix_Caching/01_README.md) | SGLang Radix Tree Trie structure, Prefix matching, LRU block eviction | [Radix Tree Cache Engine](Module_04_RadixAttention_and_Prefix_Caching/02_PROJECT_GUIDE.md) |
| **05** | [Continuous & Dynamic Batching](Module_05_Continuous_and_Dynamic_Batching/01_README.md) | Iteration-level scheduling (Orca), Slot preemption, Zero padding | [Continuous Batch Scheduler](Module_05_Continuous_and_Dynamic_Batching/02_PROJECT_GUIDE.md) |
| **06** | [Chunked Prefill & PD Disaggregation](Module_06_Chunked_Prefill_and_PD_Disaggregation/01_README.md) | Sarathi-Serve chunked prefill, Inter-token jitter elimination, Disaggregated RDMA | [Chunked Prefill & PD Simulator](Module_06_Chunked_Prefill_and_PD_Disaggregation/02_PROJECT_GUIDE.md) |
| **07** | [Speculative Decoding Architectures](Module_07_Speculative_Decoding_Architectures/01_README.md) | Rejection sampling math, Distribution preservation, Medusa tree attention | [Speculative Decoding Engine](Module_07_Speculative_Decoding_Architectures/02_PROJECT_GUIDE.md) |
| **08** | [Quantization for Serving](Module_08_Quantization_for_Serving/01_README.md) | Symmetric INT8/INT4, SmoothQuant mathematical invariance, AWQ outlier protection | [Serving Quantizer](Module_08_Quantization_for_Serving/02_PROJECT_GUIDE.md) |
| **09** | [Benchmarking & Autoscaling](Module_09_Production_Benchmarking_and_Autoscaling/01_README.md) | P99 latency percentiles, Little's Law ($L = \lambda W$), HPA autoscaler | [Serving Benchmarker](Module_09_Production_Benchmarking_and_Autoscaling/02_PROJECT_GUIDE.md) |
