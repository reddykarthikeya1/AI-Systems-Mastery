# Module 06: Troubleshooting & Edge Cases

## 1. Top 5 Production Failure Modes in Pipeline Parallelism

### Bug 1: Tied Embedding Synchronization Desync
- **Symptom**: In models where input embedding and output `lm_head` weights are tied (shared), loss fails to converge or gradients explode.
- **Root Cause**: Stage 0 hosts the input embedding and Stage $p-1$ hosts the output head. Because they reside on different physical GPUs, their gradients must be synchronized via an explicit cross-stage `All-Reduce` before the optimizer step.
- **Fix**: Register an optimizer pre-step hook that performs an all-reduce across the embedding group `[0, p-1]`.

### Bug 2: Micro-batch Count Smaller Than Pipeline Depth ($m < p$)
- **Symptom**: Pipeline bubble fraction exceeds 50%, GPU utilization is abysmal.
- **Root Cause**: If $m < p$, some GPUs never receive any work during an entire iteration.
- **Fix**: Always configure global batch size and micro-batch size such that $m \ge 4p$.
