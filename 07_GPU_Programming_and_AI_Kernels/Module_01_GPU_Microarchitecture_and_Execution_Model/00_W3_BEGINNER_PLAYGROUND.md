# 🐣 W3Schools-Style Playground: GPU Microarchitecture & Execution Model

> *"A CPU is an Olympic sprinter who can solve differential equations while running; a GPU is an army of 10,000 kindergarteners who can each color one pixel per second. If you organize them to color simultaneously, they will paint the Sistine Chapel before the sprinter laces their shoes."*

---

## 1. The Factory Analogy: SMs, Warps, and SIMT

Imagine a mega-factory building identical sports cars:
- **The Factory**: The entire GPU chip (e.g., NVIDIA H100 with 132 Streaming Multiprocessors).
- **The Assembly Floor**: A **Streaming Multiprocessor (SM)**. Each SM has its own compute ALUs, Tensor Cores, Register File, and Shared Memory (SRAM).
- **The Shift Supervisor**: The **Warp Scheduler**. It takes a crew of **32 workers (a Warp)** and issues a single instruction that all 32 workers execute at the exact same clock cycle.
- **The Rule of SIMT (Single Instruction, Multiple Threads)**: All 32 workers must perform the *exact same motion* (e.g., tighten bolt #4), but each worker holds a *different wrench on a different part of the car*.

---

## 2. Warp Divergence: The Worst Thing You Can Do to a GPU

What happens if you write code like this inside a GPU kernel?
```cpp
if (threadIdx.x % 2 == 0) {
    do_heavy_math();     // Even threads
} else {
    do_light_math();     // Odd threads
}
```

Since all 32 threads in a warp share a **single instruction unit**:
1. In Pass 1: The warp scheduler turns **OFF** the odd threads (active mask `0x55555555`). Even threads execute `do_heavy_math()`. Odd threads sit completely idle and do nothing!
2. In Pass 2: The warp scheduler turns **OFF** the even threads (active mask `0xAAAAAAAA`). Odd threads execute `do_light_math()`. Even threads sit idle!
3. **The Penalty**: The warp took the sum of *both* times! Your hardware utilization dropped by 50%.
> **Golden Rule**: Ensure all 32 threads in a warp take the same branch path. If branching is necessary, align branches to warp boundaries (multiples of 32)!

---

## 3. The Roofline Model: Are You Compute-Bound or Memory-Bound?

Every GPU kernel has a physical speed limit defined by two hardware ceilings:
1. **Peak Compute Throughput** ($P_{peak}$): e.g., 60 TFLOPs/s FP32 on an NVIDIA A100.
2. **Peak Memory Bandwidth** ($B_{peak}$): e.g., 2,000 GB/s (HBM2e).

The **Arithmetic Intensity** ($I$) is how much math you do per byte loaded from global memory (HBM):
$$I = \frac{\text{Total Operations (FLOPs)}}{\text{Total Memory Traffic (Bytes)}}$$

The **Roofline Performance Bound** ($P$):
$$P = \min(P_{peak},\; I \times B_{peak})$$

- **The Ridge Point** ($I_{ridge} = P_{peak} / B_{peak}$):
  - On an A100: $I_{ridge} = 60{,}000 \text{ GFLOPs} / 2{,}000 \text{ GB/s} = 30 \text{ FLOPs/Byte}$.
  - If your kernel has $I < 30$: You are **Memory-Bound**. Adding faster Tensor Cores will not speed up your kernel by a single microsecond; you must optimize memory coalescing and SRAM caching!
  - If your kernel has $I > 30$: You are **Compute-Bound**. You are saturating the ALUs.

---

## 4. Latency Hiding: Why GPUs Have High Occupancy

CPUs use massive L1/L2/L3 caches and speculative out-of-order branch predictors to minimize memory latency.
GPUs don't bother! When Warp 0 requests data from slow HBM (taking ~400-800 clock cycles), the Warp Scheduler **instantly switches to Warp 1 in 0 cycles**.
By the time Warps 1 through 15 have executed an instruction, Warp 0's data has arrived from HBM!
This is **Little's Law** applied to hardware:
$$\text{Concurrency (Active Warps)} = \text{Throughput} \times \text{Latency}$$
