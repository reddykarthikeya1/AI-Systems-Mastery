# Self-Assessment & Staff Interview Challenges: Profiling with NCU & NSYS

## Architectural Interview Scenarios

### Question 1: Low Occupancy with High Performance
**Scenario**: In Nsight Compute, your kernel shows only 25% theoretical occupancy, but achieves 92% of peak FP16 Tensor Core throughput. Should you optimize for higher occupancy?

**Staff-Level Solution**:
No! High occupancy is a **means to an end (latency hiding)**, not the end goal itself.
If a kernel already has sufficient Instruction-Level Parallelism (ILP)—for example, each thread computes an $8 \times 8$ micro-tile in registers—the hardware scheduler has enough independent instructions to hide memory and execution latency with only a few active warps.
Increasing occupancy by reducing register usage would reduce the micro-tile size, increase Shared Memory traffic, and lower overall throughput.
**Rule**: Never sacrifice ILP or register caching merely to chase an arbitrary occupancy percentage.
