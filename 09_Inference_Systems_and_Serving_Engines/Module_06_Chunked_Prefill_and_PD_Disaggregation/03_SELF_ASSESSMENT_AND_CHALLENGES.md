# Module 06: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: RDMA Transfer Latency vs Compute Savings in Disaggregation
**Question**: In a disaggregated serving architecture, a prefill worker generates $1.25 \text{ GB}$ of KV cache for a 4,000-token prompt. The transfer to the decode worker occurs over a 400 Gbps ($50 \text{ GB/s}$) RDMA fabric.
1. Calculate the raw network transfer time.
2. If decode TTFT SLA is $400 \text{ ms}$, evaluate whether disaggregation is viable.

**Solution**:
1. **Network Transfer Time**:
   $$T_{\text{transfer}} = \frac{1.25 \text{ GB}}{50 \text{ GB/s}} = 0.025 \text{ seconds} = 25 \text{ ms}$$
2. **Evaluation**:
   - Prefill compute time on 8x H100 $\approx 80 \text{ ms}$.
   - RDMA transmission $\approx 25 \text{ ms}$.
   - Total TTFT $\approx 80 + 25 + 10 = 115 \text{ ms} \ll 400 \text{ ms}$.
   - Disaggregation easily satisfies the TTFT SLA while completely isolating decode nodes from prefill interference!

---

### Scenario 2: Selecting Optimal Chunk Size $C$
**Question**: How does varying chunk size $C$ from 256 to 2048 tokens impact GPU arithmetic intensity and decode latency?

**Solution**:
- Small $C=256$: Minimal interference with decode ($< 15\text{ ms}$ step time), but lower prefill operational intensity ($I \approx 256$), causing prefill compute efficiency to drop.
- Large $C=2048$: High prefill compute efficiency ($I \approx 2048$), but step time increases to $> 120\text{ ms}$, causing visible decode stutter.
- Production sweet spot: $C \in [512, 1024]$ tokens.
