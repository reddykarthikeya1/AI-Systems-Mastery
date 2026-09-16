# Self-Assessment & Staff Interview Challenges: CUDA C++ Fundamentals

## Architectural Interview Scenarios

### Question 1: Host-to-Device Bottlenecks & Unified Memory
**Scenario**: An engineer replaces explicit `cudaMemcpy` with `cudaMallocManaged` (Unified Memory). Under inference, latency increases by $3\times$. Why?

**Staff-Level Solution**:
Unified Memory creates a virtual address space accessible by both CPU and GPU.
However, physical pages start on the host. When the GPU first accesses a managed pointer, a hardware **Page Fault** occurs.
The GPU hardware must stall execution, communicate with the OS virtual memory subsystem via PCIe, migrate the 4KB memory page to GPU VRAM, and invalidate host TLB entries.
For high-throughput systems, page faults introduce massive tail latency spikes.
**Fix**: Pre-fetch managed memory asynchronously before kernel launch:
`cudaMemPrefetchAsync(ptr, size, device_id, stream);` or use explicit pinned memory buffers.

---

### Question 2: Thread Block Sizing Trade-offs
**Scenario**: You can configure your kernel with `blockDim.x = 32` or `blockDim.x = 256` or `blockDim.x = 1024`. How do you choose?

**Staff-Level Solution**:
- **32 threads (1 warp)**: Low latency, but poor SM occupancy. Each SM has limits on the maximum number of active blocks (typically 32 blocks on modern GPUs). 32 blocks $\times$ 32 threads = 1,024 threads, reaching only 50% of the SM's 2,048 thread capacity.
- **1024 threads (32 warps)**: High risk of occupancy collapse due to register pressure or shared memory limits. If 1 block cannot fit, 0 blocks execute!
- **128 to 256 threads (4 to 8 warps)**: The sweet spot. Provides sufficient warps per block for latency hiding while allowing fine-grained block scheduling across SMs.
