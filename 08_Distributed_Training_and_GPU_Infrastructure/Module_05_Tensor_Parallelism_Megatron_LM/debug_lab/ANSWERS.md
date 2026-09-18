# Debug Lab Solution & Forensic Post-Mortem

## Incident: Row-Parallel Linear Layer Output Is Half the Reference Value

---

### 🔍 Forensic Root Cause Analysis
In Megatron-style row parallelism, the input-feature (reduction) dimension is split contiguously across TP ranks, and each rank computes a *partial* sum over only its own shard of that dimension -- rank 0's partial output already omits every term involving features 2 and 3, and rank 1's partial output already omits every term involving features 0 and 1. Reconstructing the full un-sharded sum therefore requires an **all-reduce SUM** across ranks: `full_output[j] = partial_rank0[j] + partial_rank1[j]`. `row_parallel_combine()` instead computes `sum(rank_partials[r][j] ...) / tp_size` -- an all-reduce **average**. Averaging two disjoint partial sums, each of which already covers a different, non-overlapping slice of the reduction dimension, is not a valid way to combine them; it divides the correct sum by `tp_size`, which is exactly the factor by which the output is short. This is distinct from an all-reduce over *redundant* copies of the same value (like gradient averaging in data parallelism), where averaging is correct precisely because every rank holds a full copy of the same quantity -- here each rank holds a genuinely different, partial contribution that must be added, not averaged.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def row_parallel_combine(rank_partials):
    tp_size = len(rank_partials)
    width = len(rank_partials[0])
    return [sum(rank_partials[r][j] for r in range(tp_size)) for j in range(width)]  # SUM, not average
```

---

### 🛡️ Production Prevention Invariants
1. **Know Which Collective Op Your Sharding Scheme Requires:** Row-parallel (reduction-dimension-sharded) layers need all-reduce SUM to combine partial sums; column-parallel (output-dimension-sharded) layers concatenate instead. Averaging is only correct when every rank redundantly holds the *same* logical quantity, as in DP gradient sync.
2. **Cross-Check Against an Un-Sharded Reference:** Always validate a tensor-parallel layer's combined output against a plain, single-device implementation of the same math on the same weights and input; a scale-only discrepancy (a clean ratio like `tp_size`) is the fingerprint of a wrong reduce op, not a logic error in the per-rank math itself.
3. **Test With `tp_size > 2`:** A discrepancy ratio that exactly equals `tp_size` is easiest to spot with more than two ranks (e.g., `tp_size=4` produces a 4x-too-small output), making the SUM-vs-AVERAGE bug unmistakable rather than a coincidental factor of two.
