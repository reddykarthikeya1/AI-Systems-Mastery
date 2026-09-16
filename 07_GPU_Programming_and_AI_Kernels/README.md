# 07. GPU Programming & AI Kernel Engineering (CUDA & Triton)

> Master the hardware-software boundary: NVIDIA GPU microarchitectures, CUDA C++, OpenAI Triton block-level programming, fused operators, FlashAttention-3, and Nsight profiling.

---

## Pedagogical Architecture: From Intuition to Principal Architect

This course is engineered to provide complete end-to-end mastery from beginner-friendly intuitions to the senior-staff/principal architecture level:
- **0 to 100 Mastery**: We deconstruct complex industry systems without skipping mathematical prerequisites or architectural trade-offs.
- **Production-Grade Blueprints**: Every module is mapped directly to systems running at scale in companies like OpenAI, Meta, Anthropic, and NVIDIA.
- **Exhaustive Rigor**: Theory, code implementations, self-assessment interview scenarios, and production troubleshooting edge cases.

---

## Master Course Roadmap

| # | Module | Architectural Scope | Resources | Status |
|---|---|---|---|:---:|
| **01** | [GPU Microarchitecture & Execution Model](Module_01_GPU_Microarchitecture_and_Execution_Model/01_README.md) | Streaming Multiprocessors (SMs), Warp Schedulers, Tensor Cores, Register Files, Shared Memory vs HBM3e, and Warp Divergence | [Playground](Module_01_GPU_Microarchitecture_and_Execution_Model/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_01_GPU_Microarchitecture_and_Execution_Model/01_README.md) · [Project](Module_01_GPU_Microarchitecture_and_Execution_Model/02_PROJECT_GUIDE.md) | 🟢 |
| **02** | [CUDA C++ Programming Fundamentals](Module_02_CUDA_Cpp_Programming_Fundamentals/01_README.md) | Kernel Launches, 3D Grid/Block/Thread Hierarchy, Thread Indexing Calculations, and Vector Addition | [Playground](Module_02_CUDA_Cpp_Programming_Fundamentals/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_02_CUDA_Cpp_Programming_Fundamentals/01_README.md) · [Project](Module_02_CUDA_Cpp_Programming_Fundamentals/02_PROJECT_GUIDE.md) | 🟢 |
| **03** | [CUDA Memory Hierarchy & Coalescing](Module_03_CUDA_Memory_Hierarchy_and_Coalescing/01_README.md) | Global Memory Coalescing Rules, Shared Memory Bank Conflicts, __syncthreads(), and Cache Bypass with LDG | [Playground](Module_03_CUDA_Memory_Hierarchy_and_Coalescing/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_03_CUDA_Memory_Hierarchy_and_Coalescing/01_README.md) · [Project](Module_03_CUDA_Memory_Hierarchy_and_Coalescing/02_PROJECT_GUIDE.md) | 🟢 |
| **04** | [Parallel Reduction & Warp Primitives](Module_04_Parallel_Reduction_and_Prefix_Sum/01_README.md) | Tree Reductions, Warp Shuffle Instructions (__shfl_down_sync), Avoiding Thread Idleness, and Inclusive/Exclusive Scan | [Playground](Module_04_Parallel_Reduction_and_Prefix_Sum/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_04_Parallel_Reduction_and_Prefix_Sum/01_README.md) · [Project](Module_04_Parallel_Reduction_and_Prefix_Sum/02_PROJECT_GUIDE.md) | 🟢 |
| **05** | [Tiled Matrix Multiplication (GEMM)](Module_05_Tiled_Matrix_Multiplication_GEMM/01_README.md) | Shared Memory Tiling, Register Tiling, Double Buffering, Matrix Transposition, and Bank Conflict Elimination | [Playground](Module_05_Tiled_Matrix_Multiplication_GEMM/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_05_Tiled_Matrix_Multiplication_GEMM/01_README.md) · [Project](Module_05_Tiled_Matrix_Multiplication_GEMM/02_PROJECT_GUIDE.md) | 🟢 |
| **06** | [OpenAI Triton Fundamentals](Module_06_OpenAI_Triton_Programming_Fundamentals/01_README.md) | Python-First Kernel Programming, Block Pointers, tl.load / tl.store with Masking, and the Triton JIT Compiler Pipeline | [Playground](Module_06_OpenAI_Triton_Programming_Fundamentals/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_06_OpenAI_Triton_Programming_Fundamentals/01_README.md) · [Project](Module_06_OpenAI_Triton_Programming_Fundamentals/02_PROJECT_GUIDE.md) | 🟢 |
| **07** | [Fused Activations & Normalization in Triton](Module_07_Fused_Activations_and_Normalization/01_README.md) | Fused LayerNorm, RMSNorm, GeLU, and Softmax with Online Max Rescaling to Prevent Overflow | [Playground](Module_07_Fused_Activations_and_Normalization/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_07_Fused_Activations_and_Normalization/01_README.md) · [Project](Module_07_Fused_Activations_and_Normalization/02_PROJECT_GUIDE.md) | 🟢 |
| **08** | [FlashAttention-1 & 2 Internals](Module_08_FlashAttention_1_and_2_Internals/01_README.md) | IO-Aware Attention Math, Tiling Q/K/V Blocks into SRAM, Online Softmax Scaling, and Avoiding O(N^2) HBM Memory Roundtrips | [Playground](Module_08_FlashAttention_1_and_2_Internals/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_08_FlashAttention_1_and_2_Internals/01_README.md) · [Project](Module_08_FlashAttention_1_and_2_Internals/02_PROJECT_GUIDE.md) | 🟢 |
| **09** | [FlashAttention-3 & Next-Gen Kernels](Module_09_FlashAttention_3_and_Hopper_Blackwell_Features/01_README.md) | Hopper TMA (Tensor Memory Accelerator), Asynchronous Data Transfers, FP8 Tensor Cores, and Ping-Pong Kernel Pipelines | [Playground](Module_09_FlashAttention_3_and_Hopper_Blackwell_Features/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_09_FlashAttention_3_and_Hopper_Blackwell_Features/01_README.md) · [Project](Module_09_FlashAttention_3_and_Hopper_Blackwell_Features/02_PROJECT_GUIDE.md) | 🟢 |
| **10** | [Quantization Kernels (FP8 & INT4)](Module_10_Quantization_Kernels_in_Triton/01_README.md) | Activation-Aware Weight Quantization (AWQ) Dequantization, FP8 E4M3 Matrix Multiplication, and INT4 Weight-Only Packed GEMM | [Playground](Module_10_Quantization_Kernels_in_Triton/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_10_Quantization_Kernels_in_Triton/01_README.md) · [Project](Module_10_Quantization_Kernels_in_Triton/02_PROJECT_GUIDE.md) | 🟢 |
| **11** | [Profiling & Kernel Tuning (NCU & NSYS)](Module_11_Profiling_with_Nsight_Compute_and_Systems/01_README.md) | Nsight Systems System-Wide Tracing, Nsight Compute Roofline Model, Memory Bandwidth Saturation, and SM Occupancy Analysis | [Playground](Module_11_Profiling_with_Nsight_Compute_and_Systems/00_W3_BEGINNER_PLAYGROUND.md) · [Theory](Module_11_Profiling_with_Nsight_Compute_and_Systems/01_README.md) · [Project](Module_11_Profiling_with_Nsight_Compute_and_Systems/02_PROJECT_GUIDE.md) | 🟢 |

---

## Verification & Honest Status

This is a **🟢 Complete Masterclass** engineered across 11 modules:
- ✅ Directory structure and roadmap for all 11 modules
- ✅ Per-module zero-anxiety W3Schools-style beginner playgrounds (`00_W3_BEGINNER_PLAYGROUND.md`)
- ✅ Production reference implementations:
  - GPU microarchitecture SIMT execution & Roofline performance bounds
  - 1D/2D/3D CUDA thread indexing and grid-stride execution
  - Memory coalescing transaction counter and shared memory 32-bank conflict detector
  - Warp shuffle register reduction and Blelloch work-efficient parallel scan
  - Tiled GEMM measuring DRAM vs SRAM memory traffic and arithmetic intensity boost
  - OpenAI Triton block-level execution engine with masked loads/stores
  - Fused RMSNorm, SwiGLU, and Online Safe Softmax
  - FlashAttention IO-aware SRAM tiling matching PyTorch bit-for-bit with $O(N)$ HBM traffic
  - Hopper TMA async tensor copy and ping-pong double buffering simulator
  - INT4 bitwise sub-byte packing/unpacking and on-the-fly dequantized GEMM
  - Nsight Compute (NCU) / Systems (NSYS) bottleneck analysis and Amdahl speedup modeling
- ✅ 100% test pass rate on reference solutions (`pytest 07_GPU_Programming_and_AI_Kernels` - 31/31 passing)
- ✅ Verified grading loop: running shipped tests against untouched stubs in `starter/` fails with `NotImplementedError`
- ✅ 0 Ruff linting errors / warnings across all code
- ✅ 100% valid relative markdown links with 0 broken links

---

## Navigation & Study Guides
- [Master Syllabus](MASTER_SYLLABUS.md)
- [Beginner Onboarding Guide](START_HERE_BEGINNER_GUIDE.md)
- [Study Plans & Pacing Guide](STUDY_PLANS_AND_PACING_GUIDE.md)
