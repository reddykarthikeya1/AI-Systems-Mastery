# Module 09: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Preventing Lustre Metadata Server (MDS) Collapse
**Question**: During checkpoint saving of an 8,192-GPU job, each GPU attempts to write its local tensors into individual per-rank files simultaneously. The storage cluster freezes, and the entire data center experiences an I/O hang. What happened at the filesystem level, and how is DCP configured to prevent this?

**Solution**:
1. **Root Cause: Metadata Server Inode Contention**:
   Parallel distributed filesystems (like Lustre or GPFS) separate Metadata Servers (MDS) from Object Storage Targets (OSTs). When 8,192 processes simultaneously open, create, and close individual files in the same directory, the MDS is bombarded with tens of thousands of POSIX metadata lock requests per second, causing metadata lock thrashing and cluster-wide filesystem collapse.
2. **Remedy: Coalesced Multi-Rank Writing**:
   - Configure DCP with **I/O consolidation**: Group ranks into I/O pools (e.g. 1 writer rank per 8-GPU node).
   - Node-local ranks copy shards to Node Rank 0 shared memory; Node Rank 0 writes a single coalesced file per node.
   - Reduces file descriptor count and file creation operations by an exact factor of 8 ($8,192 \to 1,024$).

---

### Scenario 2: Optimizer State Resharding Integrity
**Question**: When resharding an AdamW optimizer state from $TP=8$ to $TP=4$, why is simply slicing the momentum and variance tensors insufficient without tracking the internal step counter and loss scaler state?

**Solution**:
1. **State Anatomy**:
   AdamW maintains:
   - Tensor states: `exp_avg` (momentum), `exp_avg_sq` (variance), and `fp32_master_params`. These are spatially partitioned identically to model parameters.
   - Scalar states: `step` (integer step count) and `loss_scale` (dynamic loss scaling factor).
2. **Failure Mechanism**:
   If scalar states are not properly replicated or preserved during resharding, the restored optimizer resets `step = 0`. This resets the Adam bias correction factors:
   $$\beta_1^t, \quad \beta_2^t$$
   causing effective learning rate spikes by several orders of magnitude, which permanently corrupts model weights.
3. **DCP Design**: DCP treats non-tensor scalar states as replicated metadata in the global manifest, guaranteeing identical restoration across all ranks.
