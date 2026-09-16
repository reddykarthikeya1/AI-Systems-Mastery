# Module 02: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Max Concurrency Capacity Calculation
**Question**: You deploy Llama-3-70B in FP16 on a single node of 8x NVIDIA A100 (80GB) GPUs with Tensor Parallelism $TP=8$.
- Total physical VRAM across the node: $8 \times 80 = 640 \text{ GB}$.
- Model parameters occupy: $140 \text{ GB}$.
- CUDA context and activation working memory: $30 \text{ GB}$.
- Average sequence length per request: 4,096 tokens.
Calculate the maximum theoretical number of concurrent user requests the node can serve before exhausting VRAM.

**Solution**:
1. **Available KV Cache Memory**:
   $$M_{\text{available}} = 640 - 140 - 30 = 470 \text{ GB}$$
2. **KV Cache Footprint per Request**:
   For Llama-3-70B ($L=80, H_{\text{kv}}=8, d=128$):
   $$\text{Bytes per token} = 2 \times 2 \times 80 \times 8 \times 128 = 327,680 \text{ bytes} = 320 \text{ KB}$$
   For $S = 4,096$ tokens:
   $$M_{\text{req}} = 4096 \times 327,680 \text{ bytes} \approx 1.342 \times 10^9 \text{ bytes} \approx 1.25 \text{ GiB}$$
3. **Maximum Concurrent Capacity**:
   $$N_{\text{max}} = \left\lfloor \frac{470 \text{ GB}}{1.342 \text{ GB}} \right\rfloor \approx 350 \text{ concurrent requests}$$
   If static pre-allocation for $S_{\text{max}}=8192$ were used, capacity would collapse to $\approx 175$ requests regardless of actual prompt lengths!

---

### Scenario 2: FP8 KV-Cache Compression Trade-offs
**Question**: An engineer proposes casting the KV cache from BF16 to FP8 (E4M3) to double concurrent serving capacity. What are the numerical risks, and how should per-tensor vs per-head dynamic scaling factors be configured?

**Solution**:
1. **Numerical Risk**: FP8 E4M3 has only 3 mantissa bits (range $[-448, 448]$), making it vulnerable to underflow and overflow if attention logits have high variance.
2. **Configuration**:
   - Never use static per-tensor quantization; attention Key vectors frequently contain channel-specific outlier values.
   - Use **per-head dynamic scaling**: Compute $\text{scale} = \frac{448.0}{\max(|X_{\text{head}}|)}$ for each attention head independently during write, storing a single FP32 scale scalar alongside each cached block.
