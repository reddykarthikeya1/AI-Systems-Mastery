# Self-Assessment & Staff Interview Challenges: Quantization Kernels

## Architectural Interview Scenarios

### Question 1: Compute Bound vs Memory Bound Quantization Regimes
**Scenario**: When running batch size = 1 (single-user LLM generation), INT4 quantization provides a $3.5\times$ speedup. When running batch size = 256 (high-concurrency serving), INT4 quantization is often slower than FP16. Why?

**Staff-Level Solution**:
- **Batch Size = 1**: The GEMM is deeply **Memory-Bound** (Matrix-Vector multiply, $I \approx 1$). Memory bandwidth is the sole bottleneck. INT4 reduces memory traffic by $4\times$, directly speeding up execution by $\approx 3.5\times$.
- **Batch Size = 256**: The GEMM becomes **Compute-Bound** (high arithmetic intensity, $I > 100$). Memory bandwidth is no longer the bottleneck. The overhead of unpacking INT4 nibbles, converting to floats, and applying scales/zeros consumes extra ALU cycles, slowing down compute compared to native FP16 Tensor Cores.
