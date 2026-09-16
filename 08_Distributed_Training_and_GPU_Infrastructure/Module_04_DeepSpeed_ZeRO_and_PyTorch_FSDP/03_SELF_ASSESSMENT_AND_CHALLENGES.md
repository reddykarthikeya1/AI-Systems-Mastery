# Module 04: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: ZeRO-3 Throughput Degradation on Small Models
**Question**: You deploy a 7B parameter model on 64 GPUs. With standard DDP, you achieve 52% MFU (Model FLOPs Utilization). With ZeRO-3 / FSDP `FULL_SHARD`, your MFU plummets to 28%. Profile logs indicate that the GPUs spend over 40% of their execution time waiting on NCCL kernels. Why did this happen, and what exact architectural configuration will restore performance?

**Solution**:
1. **Root Cause**: A 7B parameter model requires only $\approx 14 \text{ GB}$ for weights and $\approx 112 \text{ GB}$ total static memory across all GPUs. On 64 GPUs, each GPU holds only $\approx 110 \text{M}$ parameters ($220 \text{ MB}$).
   In ZeRO-3, every single layer requires an `All-Gather` collective prior to forward GEMM and another prior to backward GEMM. For small layer weights, the collective transmission time is dominated by **NCCL latency ($\alpha$ in the $\alpha-\beta$ model)** rather than bandwidth. The GPU kernel execution finishes in microseconds, leaving the compute engine stalled waiting for the next layer's parameters.
2. **Remedy**:
   - Switch from `FULL_SHARD` to **`SHARD_GRAD_OP` (ZeRO-2)**: Optimizer states and gradients remain sharded, but model weights are persistent on each GPU. This eliminates $100\%$ of forward and backward parameter `All-Gather` collectives!
   - Alternatively, employ **Hybrid Sharding (HSDP)** with `sharding_group_size=8`: Shard parameters across the 8 GPUs inside each node (NVLink latency $< 2 \,\mu\text{s}$) and replicate across nodes.
   - Adjust `auto_wrap_policy` to wrap larger module blocks (e.g. 2–4 Transformer blocks per FSDP unit) to increase collective message sizes and amortize launch latency.

---

### Scenario 2: OOM During the Backward Pass Despite ZeRO-3
**Question**: An engineer sets `sharding_strategy=FULL_SHARD` and enables CPU offloading for optimizer states to fit a 30B model onto 8x 80GB GPUs. During the forward pass, GPU memory is stable at 38 GB. Suddenly, at step 4 of the backward pass, all ranks terminate with `CUDA out of memory`. Explain the memory dynamics causing this backward spike and how to mitigate it.

**Solution**:
1. **Root Cause**:
   - **Activation Memory Dominance**: ZeRO-3 only shards static parameters, gradients, and optimizer states. It does **not** shard activations! At batch size $B$ and sequence length $S$, activation memory scales as $O(L \cdot B \cdot S \cdot H)$.
   - **Backward Prefetch Buffer Allocation**: When `backward_prefetch=BackwardPrefetch.BACKWARD_PRE` is enabled without limit, FSDP issues `All-Gather` for layer $l-1$ while layer $l$ is still computing backward gradients. Consequently, the un-sharded weights of layer $l$, the gradients of layer $l$, the un-sharded weights of layer $l-1$, and the stored forward activations of layer $l$ are all co-resident in VRAM simultaneously.
2. **Remedy**:
   - Enable **Activation Checkpointing (Gradient Checkpointing)**: Discard intermediate activations during forward and recompute them during backward. This reduces activation memory from $O(L)$ to $O(\sqrt{L})$ or $O(1)$ per layer.
   - Set `limit_allgathers=True` in FSDP to restrict the number of concurrent in-flight all-gathers to 1.

---

### Scenario 3: Checkpoint OOM on Rank 0
**Question**: During checkpoint saving of an FSDP-sharded 70B model, the cluster crashes with a host RAM OOM error on Rank 0, while ranks 1–7 remain idle. How do you redesign the checkpointing architecture for linear scalability?

**Solution**:
1. **Root Cause**: Calling `sharded_model.state_dict()` with `StateDictType.FULL_STATE_DICT` instructs PyTorch to execute an all-gather of all sharded parameters and copy them to Rank 0 host CPU memory. Reconstructing 70B FP32 master weights on a single host node demands $> 280 \text{ GB}$ of contiguous system RAM.
2. **Remedy**:
   - Migrate to **Distributed Checkpointing (`torch.distributed.checkpoint` / DCP)** using `StateDictType.SHARDED_STATE_DICT`.
   - Each rank writes its local sharded tensor slice directly to parallel storage (e.g., Lustre/GPFS/S3) concurrently.
   - Host RAM consumption per node is bounded by $\frac{\text{Total Model Size}}{N}$, achieving $O(1)$ rank-0 memory overhead.
