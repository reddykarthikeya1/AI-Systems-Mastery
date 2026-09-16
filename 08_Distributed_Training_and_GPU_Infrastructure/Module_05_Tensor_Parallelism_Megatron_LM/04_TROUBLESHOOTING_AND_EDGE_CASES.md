# Module 05: Troubleshooting & Edge Cases

## 1. Top 5 Production Failure Modes in Tensor Parallelism

### Bug 1: Gradient Clipping Across TP Groups
- **Symptom**: Model gradients explode or training diverges unexpectedly when using `torch.nn.utils.clip_grad_norm_`.
- **Root Cause**: In Tensor Parallelism, weights are sharded. If `clip_grad_norm_` is called naively on each rank, it calculates the $L_2$ norm of only the *local slice* of weights:
  $$\text{Norm}_{\text{local}} = \sqrt{\sum \|g_{\text{local}}\|^2}$$
  Because $\text{Norm}_{\text{local}} < \text{Norm}_{\text{global}}$, the calculated scale factor $\frac{\text{max\_norm}}{\text{Norm}}$ will be incorrectly large, leading to severe under-clipping!
- **Fix**: Use Megatron's `clip_grad_norm_fp32` which performs an `All-Reduce` of sum-of-squares across the model parallel group before taking the square root.

### Bug 2: Unsynchronized LayerNorm Parameters
- **Symptom**: Rank 0 and Rank 1 diverge in weights after step 1.
- **Root Cause**: LayerNorm weights are replicated across all TP ranks. If weight decay or optimizer updates apply non-deterministic adjustments or if gradients are not averaged across the TP group, parameters diverge.
- **Fix**: Ensure LayerNorm gradients are reduced across the TP group or ensure all ranks compute identical updates.
