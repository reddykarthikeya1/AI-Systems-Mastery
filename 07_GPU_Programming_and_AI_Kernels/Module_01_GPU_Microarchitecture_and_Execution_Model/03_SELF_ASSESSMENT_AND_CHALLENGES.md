# Self-Assessment & Staff Interview Challenges: GPU Microarchitecture

## Architectural Interview Scenarios

### Question 1: Register Pressure and Occupancy Cliff
**Scenario**: You write a CUDA kernel where each thread uses 64 registers. Your thread block size is 1,024 threads.
1. What happens to SM occupancy on an NVIDIA Ampere GPU (max 65,536 registers per SM)?
2. How does the compiler handle register spills if you increase register usage to 72 registers per thread?

**Staff-Level Solution**:
1. A block of 1,024 threads using 64 registers per thread requires $1{,}024 \times 64 = 65{,}536 \text{ registers}$.
   Because an SM has exactly 65,536 registers, **only 1 block** can reside on the SM at any time.
   Active warps per SM = $1{,}024 / 32 = 32 \text{ warps}$.
   Since the SM supports a maximum of 64 warps, theoretical occupancy drops to $32 / 64 = 50\%$.
2. If register demand increases to 72, 1 block requires $1{,}024 \times 72 = 73{,}728 \text{ registers}$, which exceeds physical register file capacity!
   If unconstrained, the block cannot launch (`cudaErrorLaunchOutOfResources`).
   When compiled with `-maxrregcount`, the compiler forces **register spilling into Local Memory**.
   Local Memory is physically backed by slow L1/L2/DRAM cache lines (~400 cycles latency), severely degrading execution performance.

---

### Question 2: Memory Bound vs Compute Bound Diagnosis
**Scenario**: A junior engineer converts an FP32 matrix elementwise activation kernel ($y_i = \text{gelu}(x_i)$) to use FP16 Tensor Cores and notices 0% performance speedup. Why?

**Staff-Level Solution**:
Elementwise GeLU reads 1 input element (2 bytes in FP16) and writes 1 output element (2 bytes in FP16) while performing $\approx 8$ FLOPs.
Arithmetic intensity $I = 8 / 4 = 2.0 \text{ FLOPs/Byte}$.
On an A100, the Tensor Core ridge point is $156 \text{ FLOPs/Byte}$.
Because $2.0 \ll 156$, the kernel is deeply **Memory-Bound**—stuck waiting for HBM memory bus bandwidth.
The Tensor Cores were already idle 98% of the time waiting for memory. Accelerating compute cannot overcome memory bus saturation.
To optimize this kernel, it must be **fused** into the preceding GEMM or LayerNorm kernel.
