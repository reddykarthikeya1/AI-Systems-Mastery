# Module 05: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Continuous Batching

### Bug 1: Unsynchronized Attention Mask in Dynamic Batching
- **Symptom**: Generated completions contain random gibberish or repeat previous sentences when batch size changes dynamically.
- **Root Cause**: When adding or removing sequences from the active batch, position IDs or attention masks fail to account for differing sequence start offsets.
- **Fix**: Use FlashAttention `varlen` (variable-length) kernels with `cu_seqlens` prefix-sum arrays, avoiding flattened padded masks altogether.
