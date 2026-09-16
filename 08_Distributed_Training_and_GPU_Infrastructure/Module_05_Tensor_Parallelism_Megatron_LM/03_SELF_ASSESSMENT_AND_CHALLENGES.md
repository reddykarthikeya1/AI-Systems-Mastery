# Module 05: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Grouped-Query Attention (GQA) under High TP Degree
**Question**: You are scaling Llama-3-70B (which has $H_Q = 64$ query heads and $H_{\text{KV}} = 8$ key-value heads) on a cluster. An infrastructure engineer proposes setting Tensor Parallel degree $TP = 16$. Explain why this proposal will fail immediately, and discuss the two viable architectural remedies.

**Solution**:
1. **Root Cause**: GQA requires each TP rank to hold an integer number of KV heads:
   $$\text{Heads per rank} = \frac{H_{\text{KV}}}{TP} = \frac{8}{16} = 0.5$$
   Because a single attention head cannot be split across ranks without fine-grained internal head all-reduces, PyTorch will raise a runtime error.
2. **Architectural Remedies**:
   - **Remedy A (Cap TP to 8)**: Set $TP = 8$ (so each rank gets $64/8 = 8$ Q heads and $8/8 = 1$ KV head). Use Pipeline Parallelism ($PP = 2$ or $4$) or FSDP to scale to 16 or 32 GPUs.
   - **Remedy B (KV Head Replication)**: Replicate the 8 KV heads across the 16 ranks (each pair of ranks shares the same KV head). While functional, this increases KV activation memory redundancy.

---

### Scenario 2: Numerical Non-Determinism Across Variable TP Degrees
**Question**: When validating a model trained with $TP=2$ against a reference checkpoint trained with $TP=8$, you observe that after 5,000 steps, evaluation loss starts diverging slightly ($> 0.05$ difference). Both runs had identical global batch size, learning rate schedule, and dataset order. What is the source of this numerical divergence, and how do you ensure bitwise reproducibility?

**Solution**:
1. **Sources of Divergence**:
   - **Floating-Point Non-Associativity in All-Reduce**: Floating-point addition is non-associative: $(a + b) + c \neq a + (b + c)$. The order in which partial sums are accumulated in NCCL Ring All-Reduce depends on rank count $k$.
   - **RNG Seed Desynchronization**: In Megatron-LM, dropout masks within tensor-parallel linear layers must be partitioned differently across TP ranks, whereas data-parallel dropout must be synchronized. If RNG seeds are initialized uniformly, TP ranks will apply correlated dropout masks.
2. **Remedy**:
   - Use `megatron.core.tensor_parallel.random.TensorParallelRNGTracker` with explicit named RNG states (`tensor-parallel-seed` and `data-parallel-seed`).
   - Use deterministic collective algorithms (`NCCL_ALGO=Tree`) or enable BF16/FP32 mixed precision accumulation.

---

### Scenario 3: Inter-Node Tensor Parallelism Performance Collapse
**Question**: A junior engineer attempts to scale a 405B parameter model by setting $TP = 16$ across two 8-GPU nodes connected via 400 Gbps InfiniBand. The cluster reaches only 11% MFU. Why did MFU collapse, and what is the maximum recommended physical boundary for TP?

**Solution**:
1. **Root Cause**:
   - TP executes $2 \times \text{All-Reduce}$ collectives **per transformer layer**. In a 126-layer model, that is **252 blocking all-reduces per forward step** and **252 in backward**!
   - Intra-node NVLink latency is $\approx 1.5 \,\mu\text{s}$ with $900 \text{ GB/s}$ bi-directional bandwidth.
   - Inter-node InfiniBand latency through the host network stack is $\approx 15-25 \,\mu\text{s}$ with $50 \text{ GB/s}$ bandwidth.
   - The $10\times$ latency penalty and $18\times$ bandwidth reduction causes the GPU execution pipeline to stall in NCCL wait states for over 80% of each step.
2. **Architecture Guideline**: Tensor Parallelism must **always be confined within a single physical node** ($TP \le 8$).
