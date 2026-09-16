# Module 08: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Weight-Only Quantization (W4A16) vs Compute Speedup
**Question**: An infrastructure team quantizes a 70B model with INT4 weight-only quantization (W4A16). Benchmarks show a $2.8\times$ speedup during the decode phase, but $0\%$ speedup during the prefill phase. Explain this discrepancy using operational intensity and roofline principles.

**Solution**:
1. **Decode Phase**: Decode is memory-bandwidth bound ($I \approx 1 \text{ FLOP/byte}$). W4A16 reduces model weight footprint from $140 \text{ GB} \to 35 \text{ GB}$. Streaming $35 \text{ GB}$ over the memory bus takes $25\%$ of the time, resulting in a nearly linear speedup ($pprox 2.8\times$).
2. **Prefill Phase**: Prefill is compute-bound ($I \gg 295 \text{ FLOP/byte}$). In W4A16, INT4 weights must be dequantized to FP16 in registers before multiplying with FP16 activations on Tensor Cores. The total FLOP count remains identical, and compute throughput does not increase.
3. **Remedy for Prefill**: Use W8A8 (FP8 or INT8) matrix multiplication kernels where Tensor Cores natively execute 8-bit integer/float arithmetic at $2\times$ the TFLOPs throughput of FP16.

---

### Scenario 2: Per-Channel vs Per-Group Quantization Overhead
**Question**: Compare group size $g=128$ vs per-channel quantization in INT4. What is the metadata memory overhead?

**Solution**:
In INT4, weights take $0.5 \text{ bytes}$ per parameter.
With group size $g=128$, one FP16 scale ($2 \text{ bytes}$) is stored for every 128 weights:
$$\text{Metadata Overhead} = \frac{2 \text{ bytes}}{128 \times 0.5 \text{ bytes}} = \frac{2}{64} = 3.125\%$$
A $3.1\%$ memory overhead provides significant accuracy protection over coarse per-tensor scales.
