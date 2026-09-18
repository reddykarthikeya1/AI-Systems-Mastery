# Debug Lab Solution & Forensic Post-Mortem

## Incident: Kernel Launch Leaves Most Output Elements Unwritten

---

### 🔍 Forensic Root Cause Analysis
`compute_global_index()` returns `block_idx + thread_idx`, omitting the multiplication by `block_dim` that turns a block index into an offset into the flattened output array. The standard CUDA formula is `block_idx * block_dim + thread_idx`. Without that multiplication, `block_idx` (0-3) and `thread_idx` (0-7) simply add together, so the formula can only ever produce values from 0 to 10 -- the same small range gets hit repeatedly by many different (block, thread) pairs, while indices 11 through 31 are never produced by any thread at all.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def compute_global_index(block_idx, thread_idx, block_dim):
    return block_idx * block_dim + thread_idx
```

With the block offset correctly scaled by `block_dim`, every thread computes a distinct index covering the full 0-31 range, and the 'untouched' count drops to zero.

---

### 🛡️ Production Prevention Invariants
1. **Index Coverage Tests:** After any kernel launch (real or simulated), assert that every expected output index was written exactly once.
2. **Formula Unit Tests:** Test the global-index formula in isolation across the full grid of `(block_idx, thread_idx)` pairs and assert the resulting index set has no gaps and no duplicates.
3. **Boundary Sweeps:** Sweep small, easy-to-hand-check grid/block configurations through the indexing formula during development, before scaling up to production sizes.
