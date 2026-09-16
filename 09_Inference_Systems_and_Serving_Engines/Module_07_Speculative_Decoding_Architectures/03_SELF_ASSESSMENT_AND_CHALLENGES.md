# Module 07: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Speedup Threshold & Draft Model Sizing
**Question**: Derive the mathematical speedup condition for Speculative Decoding. Given target model latency $T_{\text{target}} = 40 \text{ ms}$, draft model latency $T_{\text{draft}} = 4 \text{ ms}$, lookahead depth $\gamma = 5$, and average token acceptance rate $\alpha = 0.75$, calculate the expected speedup.

**Solution**:
1. **Expected Accepted Tokens per Step**:
   $$\mathbb{E}[N] = \sum_{i=1}^\gamma \alpha^i + 1 = \frac{1 - \alpha^{\gamma+1}}{1 - \alpha} = \frac{1 - (0.75)^6}{1 - 0.75} = \frac{1 - 0.178}{0.25} \approx 3.29 \text{ tokens}$$
2. **Iteration Execution Time**:
   $$T_{\text{iter}} = \gamma \cdot T_{\text{draft}} + T_{\text{target}} = (5 \times 4) + 40 = 60 \text{ ms}$$
3. **Effective Latency per Token**:
   $$T_{\text{token, spec}} = \frac{60 \text{ ms}}{3.29} \approx 18.2 \text{ ms}$$
4. **Speedup**:
   $$\text{Speedup} = \frac{T_{\text{target}}}{T_{\text{token, spec}}} = \frac{40}{18.2} \approx 2.20\times$$
   The system achieves a $2.2\times$ throughput increase!

---

### Scenario 2: Acceptance Rate Collapse Under High Temperature
**Question**: An engineer reports that Speculative Decoding provides a $2.5\times$ speedup at temperature $T=0.0$ (greedy), but at $T=1.0$, speedup drops to $1.02\times$. Explain the mathematical cause of this collapse.

**Solution**:
At $T=0.0$, the draft model only needs to match the argmax of the target model. High-capacity draft models frequently agree with the target model on the top-1 token ($> 80\%$ agreement).
At $T=1.0$, rejection sampling compares full distribution probabilities: $\min(1, p(x)/q(x))$. When vocabulary size is $128\text{k}$, divergence between the distributions increases, causing rejection probability to spike and collapsing effective accepted tokens per step to $\approx 1.1$.
