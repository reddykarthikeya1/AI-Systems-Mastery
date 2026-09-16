# Module 10: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: MFU Diagnostic Analysis on 1,024 H100 GPUs
**Question**: You are training a 70B parameter model on 1,024 H100 SXM5 GPUs (peak BF16 tensor core throughput $989 \text{ TFLOPs}$ per GPU). Telemetry reports steady-state throughput of $420,000 \text{ tokens/second}$.
1. Calculate the exact MFU.
2. If the cluster cost is $3.50 per GPU-hour, calculate the hourly cost of the run and determine how much money is lost every hour compared to a world-class 50% MFU benchmark.

**Solution**:
1. **MFU Calculation**:
   $$\begin{aligned}
   \text{Theoretical FLOPs/sec achieved} &= 6 \times 70 \times 10^9 \times 420,000 = 1.764 \times 10^{17} \text{ FLOPs/sec} = 176.4 \text{ PFLOPs} \\
   \text{Total Peak Hardware FLOPs} &= 1,024 \times 989 \times 10^{12} = 1.0127 \times 10^{18} \text{ FLOPs/sec} = 1,012.7 \text{ PFLOPs} \\
   \text{MFU} &= \frac{176.4}{1012.7} \approx 0.1742 = 17.4\%
   \end{aligned}$$
   An MFU of $17.4\%$ indicates severe architectural pathology (excessive pipeline bubble, un-overlapped NCCL transfers, or CPU dataloader starvation).
2. **FinOps Impact**:
   $$\text{Hourly Run Cost} = 1,024 \times \$3.50 = \$3,584 / \text{hour}$$
   At $50\%$ MFU, the cluster would generate:
   $$\text{Target Tokens/sec} = 420,000 \times \frac{0.50}{0.1742} \approx 1,205,000 \text{ tokens/sec}$$
   To complete a 10 Trillion token run:
   - At $17.4\%$ MFU: $\frac{10^{13}}{420,000 \times 3600} \approx 6,613 \text{ hours} \implies \$23,700,000$
   - At $50.0\%$ MFU: $\frac{10^{13}}{1,205,000 \times 3600} \approx 2,305 \text{ hours} \implies \$8,260,000$
   **Total wasted expenditure: $15.44 Million!**

---

### Scenario 2: Inference Amortization vs Compute-Optimal Training
**Question**: Explain why frontier labs routinely violate Chinchilla compute-optimal ratios during pre-training.

**Solution**:
Chinchilla minimizes loss for a fixed pre-training budget $C$. It assumes training is a one-time sunk cost.
However, in production deployments:
$$\text{Total Cost} = \text{Cost}_{\text{pretrain}} + N_{\text{queries}} \times \text{Cost}_{\text{inference}}(\Phi)$$
Since inference FLOPs scale directly with $\Phi$, training a smaller model (e.g. 8B) on $100\times$ more tokens incurs slightly higher pre-training cost but lowers lifetime serving cost by $80-90\%$.
