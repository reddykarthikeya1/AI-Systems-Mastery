# Module 01: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Sizing a 70B Model Serving Cluster for Strict P99 SLA
**Question**: You are designing a real-time conversational AI system serving Llama-3-70B. The client SLA mandates:
- $P_{99} \text{ TTFT} \le 400 \text{ ms}$ for prompts up to 1,000 tokens.
- $P_{99} \text{ TPOT} \le 25 \text{ ms}$ ($40 \text{ tokens/sec}$).
Determine the minimum hardware topology (GPU count and model parallelism) required on NVIDIA H100 SXM5 GPUs ($3.35 \text{ TB/s}$ HBM3 bandwidth, $989 \text{ TFLOPs}$ BF16).

**Solution**:
1. **Decode Bandwidth Limit**:
   In FP16/BF16, 70B parameters require $140 \text{ GB}$.
   To achieve $\text{TPOT} = 25 \text{ ms}$, the memory bandwidth must be at least:
   $$\text{Required Bandwidth} = \frac{140 \text{ GB}}{0.025 \text{ s}} = 5,600 \text{ GB/s} = 5.6 \text{ TB/s}$$
   A single H100 provides $3.35 \text{ TB/s}$. Therefore, a single GPU **cannot physically satisfy the TPOT SLA**, even at batch size 1!
   With Tensor Parallelism $TP=2$:
   $$\text{Combined Bandwidth} = 2 \times 3.35 = 6.70 \text{ TB/s} > 5.6 \text{ TB/s}$$
   $$\text{Min TPOT} = \frac{140 \text{ GB}}{6.70 \text{ TB/s}} \approx 20.9 \text{ ms}$$
2. **Prefill Latency Check**:
   Computing 1,000 tokens through 70B model requires:
   $$\text{FLOPs} = 2 \times 70 \times 10^9 \times 1,000 = 1.4 \times 10^{14} \text{ FLOPs} = 140 \text{ TFLOPs}$$
   On $TP=2$ H100s ($2 \times 989 = 1,978 \text{ TFLOPs}$):
   $$\text{Compute Time} = \frac{140}{1978} \approx 70.8 \text{ ms}$$
   Adding NCCL TP communication overhead ($\approx 30 \text{ ms}$ across 80 layers), $\text{TTFT} \approx 100-150 \text{ ms} \ll 400 \text{ ms}$.
3. **Conclusion**: Minimum viable topology is **$TP=2$ H100 SXM5**.

---

### Scenario 2: Prefill Jitter (The Convoy Effect)
**Question**: An inference server in steady-state decoding at $TPOT = 22 \text{ ms}$ suddenly experiences a massive latency spike: a single token generation takes $450 \text{ ms}$. Telemetry shows a new request with a 4,000-token prompt arrived at that exact instant. Explain the systems mechanics causing this spike, and describe the industry-standard architectural solution.

**Solution**:
1. **Root Cause: Compute Starvation via Non-Chunked Prefill**:
   Standard continuous batching executes prefill and decode tasks sequentially or co-schedules them in a single iteration. When the 4,000-token prompt arrives, the engine launches a massive GEMM kernel that saturates all GPU SMs for $\approx 350-400 \text{ ms}$. Because GPU execution is non-preemptive at the hardware thread block level, the existing decode requests are blocked waiting for the prefill kernel to complete, resulting in an ITL spike from $22 \text{ ms} \to 450 \text{ ms}$.
2. **Architectural Remedy**:
   - **Chunked Prefill (Sarathi-Serve / vLLM)**: Split the 4,000-token prompt into chunks of size 512. In each iteration, schedule one 512-token prefill chunk alongside the decode batch. Bounds the iteration execution time to $< 35 \text{ ms}$.
   - **Prefill-Decode Disaggregation (PD)**: Route prefill to dedicated prefill GPU instances, and stream the generated KV-cache over RDMA to separate decode GPU instances.
