# Debug Lab Solution & Forensic Post-Mortem

## Incident: Triton-Style Vector-Add Kernel Produces Overlapping, Incorrect Blocks

---

### 🔍 Forensic Root Cause Analysis
`block_start` is computed as `pid * (BLOCK_SIZE - 1)` instead of `pid * BLOCK_SIZE`. With `BLOCK_SIZE=4`, consecutive blocks should start at offsets `0, 4, 8`, but this formula produces `0, 3, 6` -- each block overlaps the previous one by one element instead of starting exactly where it left off. The overlapping elements get written twice (harmlessly, since both writes compute the same correct value), but the accumulated one-element-per-block drift means the later blocks never reach far enough to cover the tail of the array, leaving the last positions at their initial `None` value instead of the correct sum.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def vector_add_kernel(a, b, n):
    out = [None] * n
    num_blocks = (n + BLOCK_SIZE - 1) // BLOCK_SIZE
    for pid in range(num_blocks):
        block_start = pid * BLOCK_SIZE
        for offset in range(BLOCK_SIZE):
            idx = block_start + offset
            if idx < n:
                out[idx] = a[idx] + b[idx]
    return out
```

With `block_start = pid * BLOCK_SIZE`, each program instance covers exactly its own non-overlapping slice of the array, `num_blocks * BLOCK_SIZE` collectively spans the whole array with no gaps, and every output position matches `a[i] + b[i]` with zero mismatches.

---

### 🛡️ Production Prevention Invariants
1. **Block-Offset Formula Tests:** Unit test that `pid * BLOCK_SIZE` for `pid in range(num_blocks)` produces a strictly increasing, non-overlapping partition covering `[0, n)`.
2. **Full-Array Diff in Tests:** Compare kernel output element-by-element against a plain Python reference for at least one non-block-aligned array length.
3. **Grid/Block Math Review:** Treat the `pid -> block_start` formula as the most safety-critical line in any block-partitioned kernel; review it independently of the rest of the logic.
