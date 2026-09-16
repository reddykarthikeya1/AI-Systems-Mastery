# Module 03: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Optimal Block Size Trade-Offs ($B=16$ vs $B=64$)
**Question**: Analyze the engineering trade-offs of setting physical block size $B=16$ tokens versus $B=64$ tokens in a production vLLM deployment.

**Solution**:
1. **Internal Fragmentation**:
   On average, a sequence leaves half of its final block unused:
   $$\text{Average Wasted Tokens} = \frac{B}{2}$$
   For $B=16$, average waste is 8 tokens ($pprox 2.5 \text{ MB}$ per request in 70B).
   For $B=64$, average waste is 32 tokens ($pprox 10 \text{ MB}$ per request). Small blocks minimize fragmentation.
2. **Kernel Efficiency & Block Table Overhead**:
   Smaller blocks ($B=16$) increase the length of the block table $4\times$, increasing register pressure and memory indirection overhead during the PagedAttention CUDA kernel.
   Larger blocks ($B=64$) improve memory coalescing and vector loads (`float4` / 128-bit memory instructions).
3. **Industry Consensus**: $B=16$ is optimal for variable-length conversational workloads; $B=32$ or $B=64$ is preferred for long-context batch workloads.

---

### Scenario 2: Memory Eviction: Swapping vs Recomputation
**Question**: When GPU physical blocks are completely exhausted, what are the two recovery strategies available to the scheduler, and under what sequence length conditions is each optimal?

**Solution**:
1. **Swapping (Offloading to CPU)**:
   Copy physical blocks over PCIe to host RAM ($32-64 \text{ GB/s}$). When memory frees up, swap blocks back.
   - *Advantage*: Zero duplicate computation.
   - *Cost*: PCIe latency overhead. Optimal when sequence length $S > 1,000$ tokens where prefill recomputation cost exceeds PCIe transfer time.
2. **Recomputation**:
   Discard KV blocks and preempt the request. Re-evaluate the prompt when GPU memory becomes available.
   - *Advantage*: Zero host RAM required; no PCIe bus saturation.
   - *Cost*: Wasted GPU FLOPs. Optimal for short requests ($S < 500$ tokens) where prefill finishes in $< 15 \text{ ms}$.
