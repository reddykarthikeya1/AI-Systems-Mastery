# Recommended Reading - GPU Programming and AI Kernels

Written explainers (official docs, university notes, standard references, well-known engineering blogs) for every module concept.
Each page was fetched and its text read by a script that checks the page actually names the concepts listed under `Covers`.
Use these when a video is not enough or you prefer text; then do the module exercises.

### Module 01: GPU Microarchitecture & Execution Model

- [CUDA - Wikipedia](https://en.wikipedia.org/wiki/CUDA) | **en.wikipedia.org** | Covers: GPU Microarchitecture, Execution Model
- [CUDA Programming Guide — CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html) | **docs.nvidia.com** | Covers: Execution Model
- [NVIDIA Hopper Architecture In-Depth | NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) | **developer.nvidia.com** | Covers: Execution Model
- [Hopper (microarchitecture) - Wikipedia](https://en.wikipedia.org/wiki/Hopper_(microarchitecture)) | **en.wikipedia.org** | Covers: GPU Microarchitecture

### Module 02: CUDA C++ Programming Fundamentals

- [An Even Easier Introduction to CUDA (Updated) | NVIDIA Technical Blog](https://developer.nvidia.com/blog/even-easier-introduction-cuda/) | **developer.nvidia.com** | Covers: CUDA C++ Programming Fundamentals
- [CUDA Best Practices Guide — CUDA C++ Best Practices Guide 13.4 documentation](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) | **docs.nvidia.com** | Covers: CUDA C++ Programming Fundamentals
- [CUDA Programming Guide — CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html) | **docs.nvidia.com** | Covers: CUDA C++ Programming Fundamentals

### Module 03: CUDA Memory Hierarchy & Coalescing

- [How to Access Global Memory Efficiently in CUDA C/C++ Kernels | NVIDIA Technical Blog](https://developer.nvidia.com/blog/how-access-global-memory-efficiently-cuda-c-kernels/) | **developer.nvidia.com** | Covers: Coalescing
- [CUDA - Wikipedia](https://en.wikipedia.org/wiki/CUDA) | **en.wikipedia.org** | Covers: CUDA Memory Hierarchy
- [Using Shared Memory in CUDA C/C++ | NVIDIA Technical Blog](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/) | **developer.nvidia.com** | Covers: Coalescing
- [CUDA Best Practices Guide — CUDA C++ Best Practices Guide 13.4 documentation](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#memory-optimizations) | **docs.nvidia.com** | Covers: Coalescing

### Module 04: Parallel Reduction & Warp Primitives

- [Using CUDA Warp-Level Primitives | NVIDIA Technical Blog](https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/) | **developer.nvidia.com** | Covers: Parallel Reduction, Warp Primitives
- [Faster Parallel Reductions on Kepler | NVIDIA Technical Blog](https://developer.nvidia.com/blog/faster-parallel-reductions-kepler/) | **developer.nvidia.com** | Covers: Parallel Reduction

### Module 05: Tiled Matrix Multiplication (GEMM)

- [Matrix Multiplication Background User's Guide - NVIDIA Docs](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) | **docs.nvidia.com** | Covers: Tiled Matrix Multiplication, GEMM
- [CUTLASS: Fast Linear Algebra in CUDA C++ | NVIDIA Technical Blog](https://developer.nvidia.com/blog/cutlass-linear-algebra-cuda/) | **developer.nvidia.com** | Covers: Tiled Matrix Multiplication, GEMM
- [How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) | **siboehm.com** | Covers: GEMM

### Module 06: OpenAI Triton Programming Fundamentals

- [Vector Addition — Triton documentation](https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html) | **triton-lang.org** | Covers: OpenAI Triton Programming Fundamentals
- [Matrix Multiplication — Triton documentation](https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html) | **triton-lang.org** | Covers: OpenAI Triton Programming Fundamentals
- [Introducing Triton: Open-source GPU programming for neural networks | OpenAI](https://openai.com/index/triton/) | **openai.com** | Covers: OpenAI Triton Programming Fundamentals

### Module 07: Fused Activations & Normalization Kernels

- [Layer Normalization — Triton documentation](https://triton-lang.org/main/getting-started/tutorials/05-layer-norm.html) | **triton-lang.org** | Covers: Normalization Kernels
- [Making Deep Learning go Brrrr From First Principles](https://horace.io/brrr_intro.html) | **horace.io** | Covers: Fused Activations

### Module 08: FlashAttention-1 & 2 Internals

- [[2205.14135] FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) | **arxiv.org** | Covers: FlashAttention-1
- [[2307.08691] FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) | **arxiv.org** | Covers: FlashAttention-1
- [Stanford CRFM](https://crfm.stanford.edu/2023/07/17/flash2.html) | **crfm.stanford.edu** | Covers: FlashAttention-1
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision | Tri Dao](https://tridao.me/blog/2024/flash3/) | **tridao.me** | Covers: FlashAttention-1

### Module 09: FlashAttention-3 & Hopper/Blackwell Innovations

- [The Engine Behind AI Factories | NVIDIA Blackwell Architecture](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) | **nvidia.com** | Covers: FlashAttention-3, Hopper, Blackwell Innovations
- [Blackwell (microarchitecture) - Wikipedia](https://en.wikipedia.org/wiki/Blackwell_(microarchitecture)) | **en.wikipedia.org** | Covers: FlashAttention-3, Hopper, Blackwell Innovations
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision | Tri Dao](https://tridao.me/blog/2024/flash3/) | **tridao.me** | Covers: FlashAttention-3, Hopper
- [NVIDIA Hopper Architecture In-Depth | NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) | **developer.nvidia.com** | Covers: FlashAttention-3, Hopper
- [[2407.08608] FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) | **arxiv.org** | Covers: FlashAttention-3

### Module 10: Quantization Kernels in Triton (FP8 & INT4)

- [INT4 Decoding GQA CUDA Optimizations for LLM Inference – PyTorch](https://pytorch.org/blog/int4-decoding/) | **pytorch.org** | Covers: Quantization Kernels in Triton, FP8, INT4
- [Overview · Hugging Face](https://huggingface.co/docs/transformers/quantization/overview) | **huggingface.co** | Covers: FP8, INT4
- [Accelerating Triton Dequantization Kernels for GPTQ – PyTorch](https://pytorch.org/blog/accelerating-triton/) | **pytorch.org** | Covers: Quantization Kernels in Triton, INT4
- [[2209.05433] FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433) | **arxiv.org** | Covers: FP8
- [Floating-Point 8: An Introduction to Efficient, Lower-Precision AI Training | NVIDIA Technical Blog](https://developer.nvidia.com/blog/floating-point-8-an-introduction-to-efficient-lower-precision-ai-training/) | **developer.nvidia.com** | Covers: FP8

### Module 11: Profiling & Tuning with Nsight (NCU & NSYS)

- [User Guide — Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/index.html) | **docs.nvidia.com** | Covers: Profiling, Tuning with Nsight, NCU, NSYS
- [4. Nsight Compute — NsightCompute](https://docs.nvidia.com/nsight-compute/NsightCompute/index.html) | **docs.nvidia.com** | Covers: Profiling, Tuning with Nsight, NCU
- [2. Profiling Guide — NsightCompute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html) | **docs.nvidia.com** | Covers: Profiling, Tuning with Nsight, NCU
- [Using Nsight Compute to Inspect your Kernels | NVIDIA Technical Blog](https://developer.nvidia.com/blog/using-nsight-compute-to-inspect-your-kernels/) | **developer.nvidia.com** | Covers: Profiling, Tuning with Nsight
- [Nsight Compute | NVIDIA Developer](https://developer.nvidia.com/nsight-compute) | **developer.nvidia.com** | Covers: Profiling, Tuning with Nsight
