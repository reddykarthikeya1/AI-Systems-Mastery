# Debug Lab Solution & Forensic Post-Mortem

## Incident: Ring All-Reduce Mean Gradient Is 4x Too Small

---

### 🔍 Forensic Root Cause Analysis
`reduce_scatter_sum()` already divides by `world_size` before returning (`summed_chunks.append(total / world_size)`), so its result is already the per-chunk *mean* across ranks, not a raw sum -- despite the collective normally being described as a "reduce-scatter sum." `ring_allreduce_mean()` then divides that already-averaged result by `world_size` a second time (`return [v / world_size for v in reduced]`), under the assumption that `reduce_scatter_sum()` returns an unnormalized sum that still needs averaging. The two functions disagree about which one owns the division by `world_size`, and because both apply it, the final gradient is scaled down by `world_size ** 2` relative to the true sum instead of `world_size ** 1` -- i.e., it is `1/world_size` times the correct mean. This is a classic double-normalization bug at a collective-communication boundary: it is invisible in a single-function unit test of either piece in isolation and only shows up once the two are composed.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def reduce_scatter_sum(rank_buffers):
    world_size = len(rank_buffers)
    chunk_count = len(rank_buffers[0])
    summed_chunks = []
    for c in range(chunk_count):
        total = sum(rank_buffers[r][c] for r in range(world_size))
        summed_chunks.append(total)  # raw sum -- no normalization here
    return summed_chunks


def ring_allreduce_mean(rank_buffers):
    world_size = len(rank_buffers)
    reduced = reduce_scatter_sum(rank_buffers)
    return [v / world_size for v in reduced]  # the only division by world_size
```

---

### 🛡️ Production Prevention Invariants
1. **One Function Owns Each Normalization:** Document explicitly, in the function's contract (docstring or type), whether it returns a raw sum or an already-averaged value, and normalize in exactly one place along any reduction pipeline.
2. **Unit-Test the Composition, Not Just the Parts:** A test that calls `reduce_scatter_sum()` alone and a test that calls `ring_allreduce_mean()` alone can each look correct in isolation; add an end-to-end test asserting the final output equals `sum(all gradients) / world_size`.
3. **Sanity-Check Against `world_size` Scaling:** When a collective's output is suspiciously smaller (or larger) than expected, check whether the ratio matches `world_size` or `world_size ** 2` before looking anywhere else -- that ratio is the fingerprint of a missing or duplicated averaging step.
