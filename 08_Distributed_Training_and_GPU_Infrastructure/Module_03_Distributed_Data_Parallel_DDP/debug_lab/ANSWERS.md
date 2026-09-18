# Debug Lab Solution & Forensic Post-Mortem

## Incident: DDP Effective Gradient Scales Up With Accumulation Steps

---

### 🔍 Forensic Root Cause Analysis
`local_accumulated_grad()` sums (does not average) a rank's `accumulation_steps` microbatch gradients into one local buffer before the cross-rank sync point -- this is the correct, standard way to implement gradient accumulation locally. `allreduce_average()` then averages that already-summed-over-microbatches buffer across ranks only, dividing by `world_size`. Nothing in the pipeline ever divides by `accumulation_steps`. The result is a gradient that is the sum of `accumulation_steps` individual microbatch gradients (averaged only across ranks, not across the accumulation window), which is `accumulation_steps` times larger than the mean gradient a single large batch of that combined size should produce. Left unnoticed, this silently multiplies the effective learning rate by `accumulation_steps` every time gradient accumulation is enabled or its step count is changed, producing training instability (or outright divergence) that looks like a bad learning-rate choice rather than a normalization bug.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def ddp_step_gradient(per_rank_microbatch_grads):
    accumulation_steps = len(per_rank_microbatch_grads[0])
    accumulated = [local_accumulated_grad(mb) for mb in per_rank_microbatch_grads]
    synced = allreduce_average(accumulated)
    return [v / accumulation_steps for v in synced]  # normalize over the accumulation window too
```

---

### 🛡️ Production Prevention Invariants
1. **Normalize Over Every Averaging Dimension:** When a gradient is both accumulated over microbatches and synced over ranks, both dimensions must be divided out somewhere in the pipeline -- accumulation steps and world size are independent normalization factors, not substitutes for each other.
2. **Test With Accumulation Steps > 1:** A pipeline test that only exercises `accumulation_steps=1` can never catch a missing accumulation-window division; always include a test with `accumulation_steps > 1` and identical per-microbatch gradients so the expected effective gradient is trivially predictable.
3. **Watch the Effective-Batch-Size / Learning-Rate Relationship:** Whenever accumulation steps or world size change, verify the effective gradient magnitude stays consistent with a fixed effective learning rate; an unexplained scale factor tracking one of those knobs is the signature of a missing normalization.
