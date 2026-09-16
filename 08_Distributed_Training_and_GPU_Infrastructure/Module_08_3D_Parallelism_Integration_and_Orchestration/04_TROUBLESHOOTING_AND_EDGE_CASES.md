# Module 08: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in 3D Parallelism

### Bug 1: Cartesian Communicator Rank Permutation Bug
- **Symptom**: Collective calls hang indefinitely during process group initialization.
- **Root Cause**: If Rank 0 builds groups with order `(TP, PP, DP)` and Rank 1 builds groups with order `(DP, PP, TP)`, ranks disagree on collective membership.
- **Fix**: Centralize process group creation using strict bijective coordinate mappings.

### Bug 2: DP Gradient Sync Omission in Micro-batched PP
- **Symptom**: Loss diverges; DP replicas fail to learn.
- **Root Cause**: In 1F1B, gradients accumulate across $m$ micro-batches. If DP reduction is triggered on every microbatch instead of once per iteration, communication volume explodes $m\times$ and gradients are scaled incorrectly.
- **Fix**: Accumulate gradients across all $m$ microbatches and execute DP synchronization only during the final cooldown phase.
