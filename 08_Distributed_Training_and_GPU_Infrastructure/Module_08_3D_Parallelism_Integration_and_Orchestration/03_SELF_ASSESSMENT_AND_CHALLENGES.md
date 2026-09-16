# Module 08: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Optimal 3D Grid Topology Sizing for 530B Model
**Question**: You are tasked with training a 530B parameter Transformer model across 2,048 H100 GPUs (256 nodes, 8 GPUs per node, 3.2 Tbps InfiniBand per node). Determine the optimal configuration of $(TP, PP, DP)$ to achieve maximum MFU while avoiding VRAM OOM. Justify your choice against alternatives.

**Solution**:
1. **Hardware Constraints**:
   - Intra-node NVLink bandwidth is $900 \text{ GB/s}$.
   - Inter-node InfiniBand bandwidth is $400 \text{ Gbps} = 50 \text{ GB/s}$ per GPU.
   - Rule: $TP$ must not exceed node boundary $\implies TP = 8$.
2. **Pipeline Parallel Dimension**:
   - Model layers $L = 105$.
   - If $PP = 16$, layers per stage $L / PP = 105 / 16 \approx 6.5$ layers per GPU.
   - Bubble fraction with $m = 64$ micro-batches: $F_{\text{bubble}} = \frac{16 - 1}{64} \approx 23\%$.
   - If $PP = 8$, layers per stage $\approx 13$. Bubble fraction $F_{\text{bubble}} = \frac{7}{64} \approx 10.9\%$.
   - Memory per GPU with $TP=8, PP=8$: $\frac{16 \times 530}{64} = 132.5 \text{ GB}$. This exceeds 80 GB!
   - Therefore, we must choose $PP = 16$ or use $PP = 8$ with **ZeRO-1 / ZeRO-2 enabled on the DP group**!
3. **Optimal Selection**:
   - Set **$TP = 8$** (within node), **$PP = 8$**, **$DP = 32$** ($8 \times 8 \times 32 = 2,048$).
   - Enable **ZeRO-1** on the $DP=32$ group. Static memory per GPU drops to:
     $$M_{\text{GPU}} = \frac{4\Phi}{TP \cdot PP} + \frac{12\Phi}{TP \cdot PP \cdot DP} = \frac{2120}{64} + \frac{6360}{2048} = 33.1 + 3.1 = 36.2 \text{ GB}!$$
   - Fits easily inside 80 GB with 43.8 GB reserved for activations! Bubble fraction is bounded at $10.9\%$.

---

### Scenario 2: Straggler Amplification in 3D Parallelism
**Question**: Telemetry detects that GPU Rank 47 exhibits a 6% thermal throttling slowdown. How does this single-GPU performance degradation propagate across the remaining 2,047 GPUs in a 3D parallel cluster?

**Solution**:
1. **TP Propagation**: Rank 47 performs $2 \times \text{All-Reduce}$ collectives on every layer with its 7 TP peers. The TP peers stall waiting for Rank 47 on every single layer, throttled immediately to $-6\%$.
2. **PP Propagation**: The pipeline stage hosting Rank 47 finishes late, delaying activation handoff to the next downstream stage. All 16 pipeline stages serialize on the slowest stage.
3. **DP Propagation**: At the gradient reduction phase, all 32 DP replicas must synchronize gradients.
4. **Global Impact**: A $6\%$ slowdown on one GPU throttles the entire 2,048 GPU cluster by $\approx 6\%$, burning hundreds of thousands of dollars in wasted compute. Automated telemetry must immediately cordon the node and trigger restart from DCP.
