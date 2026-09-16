# 🐣 Interactive Foundations Playground: Profiling & Kernel Tuning (NCU & NSYS)

> *"Optimizing a GPU kernel without profiling is like driving at 200 mph with your eyes closed. You might feel fast until you slam head-first into a memory bus bottleneck."*

---

## 1. Top-Down vs Bottom-Up Profiling

Professional AI systems engineers use a two-phase diagnostic strategy:
1. **Top-Down System Tracing: Nsight Systems (`nsys`)**
   - Captures the entire system timeline: CPU threads, CUDA runtime calls, NCCL collective communications, and GPU kernel executions.
   - **What you look for**:
     - GPU idle bubbles (gaps between kernels).
     - CPU launch overhead (Python bytecode bottlenecks).
     - Host-to-device `cudaMemcpy` blocking the pipeline.
2. **Bottom-Up Kernel Deep Dive: Nsight Compute (`ncu`)**
   - Instruments individual GPU kernels down to the instruction and cycle level.
   - **What you look for**:
     - Speed of Light (SOL) % of peak compute and peak memory bandwidth.
     - Warp issue stall reasons.
     - Register pressure and shared memory bank conflicts.

---

## 2. Deciphering NCU Warp Stall Categories

Inside each Streaming Multiprocessor (SM), why do warps sit stalled?
- **`stall_long_scoreboard` (DRAM Latency)**: Warps are waiting for global memory (HBM) data to arrive.
  - *Fix*: Increase active warps (occupancy) to hide latency; vectorize memory reads (`float4`); ensure 128-byte coalescing.
- **`stall_short_scoreboard` (SRAM Latency)**: Warps are waiting for Shared Memory data.
  - *Fix*: Eliminate shared memory bank conflicts; increase Instruction-Level Parallelism (ILP).
- **`stall_barrier` (Synchronization)**: Warps are halted at `__syncthreads()`.
  - *Fix*: Remove unnecessary barriers; use warp-level shuffle instructions (`__shfl_down_sync`).
- **`stall_math_pipe_throttle` (Compute Saturation)**: The ALUs/Tensor Cores are running at 100% capacity!
  - *Status*: Your kernel is Compute-Bound! You have reached peak hardware performance.
