# Recommended Reading - Inference Systems and Serving Engines

Written explainers (official docs, university notes, standard references, well-known engineering blogs) for every module concept.
Each page was fetched and its text read by a script that checks the page actually names the concepts listed under `Covers`.
Use these when a video is not enough or you prefer text; then do the module exercises.

### Module 01: Inference Latency, TTFT & TPOT Trade-offs

- [Reproducible Performance Metrics for LLM inference](https://www.anyscale.com/blog/reproducible-performance-metrics-for-llm-inference) | **anyscale.com** | Covers: Inference Latency, TTFT, TPOT Trade-offs
- [Benchmarking Text Generation Inference](https://huggingface.co/blog/tgi-benchmarking) | **huggingface.co** | Covers: Inference Latency, TTFT, TPOT Trade-offs
- [Metrics — NVIDIA NIM LLMs Benchmarking](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) | **docs.nvidia.com** | Covers: TTFT, TPOT Trade-offs
- [Achieve 23x LLM Inference Throughput & Reduce p50 Latency](https://www.anyscale.com/blog/continuous-batching-llm-inference) | **anyscale.com** | Covers: Inference Latency, TPOT Trade-offs
- [Optimizing inference · Hugging Face](https://huggingface.co/docs/transformers/main/en/llm_optims) | **huggingface.co** | Covers: Inference Latency, TPOT Trade-offs

### Module 02: KV-Cache Memory Hierarchy & Growth

- [Cache strategies · Hugging Face](https://huggingface.co/docs/transformers/main/en/kv_cache) | **huggingface.co** | Covers: Growth
- [Mastering LLM Techniques: Inference Optimization | NVIDIA Technical Blog](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/) | **developer.nvidia.com** | Covers: KV-Cache Memory Hierarchy
- [Large Transformer Model Inference Optimization | Lil'Log](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/) | **lilianweng.github.io** | Covers: Growth

### Module 03: PagedAttention Architecture (vLLM)

- [vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention | vLLM Blog](https://vllm.ai/blog/2023-06-20-vllm) | **blog.vllm.ai** | Covers: PagedAttention Architecture, vLLM
- [[2309.06180] Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) | **arxiv.org** | Covers: PagedAttention Architecture, vLLM
- [vLLM](https://docs.vllm.ai/en/latest/) | **docs.vllm.ai** | Covers: vLLM

### Module 04: RadixAttention & Prefix Caching (SGLang)

- [Fast and Expressive LLM Inference with RadixAttention and SGLang - LMSYS Org](https://www.lmsys.org/blog/2024-01-17-sglang/) | **lmsys.org** | Covers: RadixAttention, SGLang
- [Automatic Prefix Caching - vLLM](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) | **docs.vllm.ai** | Covers: Prefix Caching
- [[2312.07104] SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104) | **arxiv.org** | Covers: SGLang
- [Welcome to SGLang - SGLang Documentation](https://docs.sglang.io/) | **docs.sglang.ai** | Covers: SGLang

### Module 05: Continuous & Dynamic Iteration-Level Batching

- [Achieve 23x LLM Inference Throughput & Reduce p50 Latency](https://www.anyscale.com/blog/continuous-batching-llm-inference) | **anyscale.com** | Covers: Continuous, Dynamic Iteration-Level Batching
- [LLM Inference at scale with TGI](https://huggingface.co/blog/martinigoyanes/llm-inference-at-scale-with-tgi) | **huggingface.co** | Covers: Continuous

### Module 06: Chunked Prefill & Prefill-Decode (PD) Disaggregation

- [[2401.09670] DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Mod](https://arxiv.org/abs/2401.09670) | **arxiv.org** | Covers: Prefill-Decode, PD, Disaggregation
- [Throughput is Not All You Need: Maximizing Goodput in LLM Serving using Prefill-Decode Disaggregatio](https://haoailab.com/blogs/distserve/) | **hao-ai-lab.github.io** | Covers: Chunked Prefill, Prefill-Decode, Disaggregation
- [[2308.16369] SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills](https://arxiv.org/abs/2308.16369) | **arxiv.org** | Covers: Chunked Prefill, Prefill-Decode, PD
- [vLLM](https://docs.vllm.ai/en/latest/) | **docs.vllm.ai** | Covers: Prefill-Decode

### Module 07: Speculative Decoding & Medusa Multi-Head Verification

- [Medusa: Simple framework for accelerating LLM generation with multiple decoding heads](https://www.together.ai/blog/medusa) | **together.ai** | Covers: Speculative Decoding, Medusa Multi-Head Verification
- [GitHub - FasterDecoding/Medusa: Medusa: Simple Framework for Accelerating LLM Generation with Multip](https://github.com/FasterDecoding/Medusa) | **github.com** | Covers: Speculative Decoding, Medusa Multi-Head Verification
- [[2211.17192] Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) | **arxiv.org** | Covers: Speculative Decoding
- [[2401.10774] Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) | **arxiv.org** | Covers: Medusa Multi-Head Verification
- [Looking back at speculative decoding](https://research.google/blog/looking-back-at-speculative-decoding/) | **research.google** | Covers: Speculative Decoding

### Module 08: Model Quantization for Serving (FP8, AWQ, Marlin)

- [Quantization - vLLM](https://docs.vllm.ai/en/latest/features/quantization/index.html) | **docs.vllm.ai** | Covers: Model Quantization for Serving, FP8, AWQ
- [[2408.11743] MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models](https://arxiv.org/abs/2408.11743) | **arxiv.org** | Covers: Model Quantization for Serving, Marlin
- [Overview · Hugging Face](https://huggingface.co/docs/transformers/quantization/overview) | **huggingface.co** | Covers: Model Quantization for Serving, FP8
- [[2306.00978] AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/abs/2306.00978) | **arxiv.org** | Covers: AWQ

### Module 09: Production Benchmarking, SLAs & Autoscaling

- [A Comprehensive Guide to NIM LLM Latency-Throughput Benchmarking — NVIDIA NIM LLMs Benchmarking](https://docs.nvidia.com/nim/benchmarking/llm/latest/index.html) | **docs.nvidia.com** | Covers: Production Benchmarking
- [Google SRE - Defining slo: service level objective meaning](https://sre.google/sre-book/service-level-objectives/) | **sre.google** | Covers: SLAs
- [Horizontal Pod Autoscaling | Kubernetes](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) | **kubernetes.io** | Covers: Autoscaling
- [Ray Serve Autoscaling — Ray 2.58.0](https://docs.ray.io/en/latest/serve/autoscaling-guide.html) | **docs.ray.io** | Covers: Autoscaling
