# 09. AI Inference Systems & Serving Engines

> **The Definitive 10/10 Production Masterclass**: High-throughput, low-latency LLM serving engines at scale. Covers vLLM PagedAttention, physical block allocation, SGLang RadixAttention prefix caching, continuous / iteration-level batching, chunked prefill, disaggregated prefill-decode (PD) serving, speculative decoding, model quantization (FP8, INT4 AWQ, SmoothQuant, Marlin), and production SLA capacity planning.

---

## Pedagogical Architecture: From Intuition to Principal Inference Architect

- **00_FOUNDATIONS_PLAYGROUND.md**: Zero-jargon visual analogies, virtual memory metaphors, and runnable Python snippets.
- **01_README.md**: Rigorous mathematical expositions, roofline operational intensity derivations, and kernel memory mechanics.
- **02_PROJECT_GUIDE.md**: Production design blueprints and architectural invariants.
- **03_SELF_ASSESSMENT_AND_CHALLENGES.md**: 5 Staff/Principal AI Serving interview scenarios with detailed mathematical solutions.
- **04_TROUBLESHOOTING_AND_EDGE_CASES.md**: Real production post-mortems (thermal throttling, memory fragmentation, lock contention, cold starts).
- **project_solution/**: Deterministic, verified Python/NumPy simulation engines.
- **starter/**: Clean student stubs enforcing the strict grading-loop invariant.

---

## Master Course Roadmap

| # | Module | Core Architectural Scope | Deliverables & Code Engines | Status |
|---|---|---|---|:---:|
| **01** | [Inference Latency & Throughput Trade-offs](Module_01_Inference_Latency_Throughput_Tradeoffs/01_README.md) | TTFT vs TPOT Pareto frontier, compute-bound prefill vs memory-bandwidth bound decode, and roofline analysis | [Inference Metrics Simulator](Module_01_Inference_Latency_Throughput_Tradeoffs/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **02** | [KV-Cache Memory Management](Module_02_KV_Cache_Memory_Management/01_README.md) | Attention KV-tensor footprint ($2\times 2 \times L \times H \times d \times S$), MHA vs GQA vs MQA, and memory fragmentation | [KV Cache Allocator](Module_02_KV_Cache_Memory_Management/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **03** | [PagedAttention Architecture (vLLM)](Module_03_PagedAttention_Architecture_vLLM/01_README.md) | OS virtual memory paging, block tables, Copy-on-Write (CoW) parallel sampling, and fragmentation elimination | [PagedAttention Block Manager](Module_03_PagedAttention_Architecture_vLLM/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **04** | [RadixAttention & Prefix Caching](Module_04_RadixAttention_and_Prefix_Caching/01_README.md) | SGLang Radix Tree Trie-based KV-cache reuse, longest prefix matching, and LRU block eviction policies | [Radix Tree Cache Engine](Module_04_RadixAttention_and_Prefix_Caching/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **05** | [Continuous & Dynamic Batching](Module_05_Continuous_and_Dynamic_Batching/01_README.md) | Orca iteration-level scheduling, early departure, zero-padding execution, and dynamic token admission | [Continuous Batch Scheduler](Module_05_Continuous_and_Dynamic_Batching/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **06** | [Chunked Prefill & PD Disaggregation](Module_06_Chunked_Prefill_and_PD_Disaggregation/01_README.md) | Sarathi-Serve chunked prefill, inter-token jitter mitigation, and disaggregated RDMA prefill-decode serving | [Chunked Prefill & PD Simulator](Module_06_Chunked_Prefill_and_PD_Disaggregation/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **07** | [Speculative Decoding Architectures](Module_07_Speculative_Decoding_Architectures/01_README.md) | Leviathan rejection sampling with exact distribution preservation, Medusa multi-head speculation, and tree attention | [Speculative Decoding Engine](Module_07_Speculative_Decoding_Architectures/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **08** | [Quantization for Serving](Module_08_Quantization_for_Serving/01_README.md) | Symmetric INT8/INT4 quantization, SmoothQuant activation outlier migration, AWQ, and Marlin packed kernels | [Serving Quantizer](Module_08_Quantization_for_Serving/02_PROJECT_GUIDE.md) | 🟢 Complete |
| **09** | [Benchmarking & Autoscaling](Module_09_Production_Benchmarking_and_Autoscaling/01_README.md) | Percentile telemetry ($P_{50}, P_{90}, P_{99}$), Little's Law capacity planning ($L = \lambda W$), and HPA metrics | [Serving Benchmarker](Module_09_Production_Benchmarking_and_Autoscaling/02_PROJECT_GUIDE.md) | 🟢 Complete |

---

## Testing & Verification

```powershell
# Run interactive quickstart demonstration across all modules
python 00_quickstart_interactive_demo.py

# Run full automated test suite
pytest 09_Inference_Systems_and_Serving_Engines -v
ruff check 09_Inference_Systems_and_Serving_Engines
```
