# Debug Lab Solution & Forensic Post-Mortem

## Incident: Warp Completion Latency Estimator Undercounts Divergent Branches

---

### 🔍 Forensic Root Cause Analysis
`simulate_warp_naive()` computes `max(costs)` across all 32 lanes, which implicitly assumes that threads taking different branches execute *concurrently* -- as if the 'if' lanes and 'else' lanes were independent warps running in parallel. On real SIMT hardware, however, every thread in a warp shares a single instruction stream: when the warp diverges, the hardware serially executes the 'if' path with the 'else'-lanes masked off, then serially executes the 'else' path with the 'if'-lanes masked off. The true warp latency for a two-way divergent branch is the *sum* of both paths' costs, not the max, because divergence forces serialization rather than eliminating it.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def simulate_warp_naive(thread_predicates, cost_if, cost_else):
    took_if = any(thread_predicates)
    took_else = any(not p for p in thread_predicates)
    total = 0
    if took_if:
        total += cost_if
    if took_else:
        total += cost_else
    return total
```

Once the estimator accounts for serialized execution of both divergent paths, its output matches the correct 10-cycle total instead of undercounting the warp's real latency.

---

### 🛡️ Production Prevention Invariants
1. **Model Divergence Explicitly:** Any warp-level cost model must serialize divergent branch paths rather than taking a max/parallel assumption across lanes.
2. **Cross-Check Against Profiler Counters:** Validate cost-model estimates against real branch-efficiency / divergent-branch counters from a profiler on representative kernels.
3. **Regression on Known Divergence Patterns:** Keep a small suite of predicate patterns (all-same, half-half, one-outlier) with hand-computed expected latencies as a standing test of the cost model.
