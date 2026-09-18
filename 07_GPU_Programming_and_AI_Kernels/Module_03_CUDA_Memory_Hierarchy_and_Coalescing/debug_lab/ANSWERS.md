# Debug Lab Solution & Forensic Post-Mortem

## Incident: Contiguous-Looking Row Read Triggers One Memory Transaction Per Lane

---

### 🔍 Forensic Root Cause Analysis
`compute_address(row, col, cols)` computes the flat offset as `(col * cols + row) * dtype_size` -- but for a row-major matrix the correct flat offset is `(row * cols + col) * dtype_size`; `row` and `col` are transposed in the formula. `warp_access_pattern()` varies `lane` through the `col` parameter, intending for consecutive lanes to read consecutive elements of row 0. Because of the transposition, consecutive lanes instead land on addresses that are `cols` elements (`128` bytes) apart -- each lane's address falls in its own separate 32-byte segment, so every lane demands its own memory transaction instead of 32 lanes sharing a handful of transactions.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def compute_address(row, col, cols, dtype_size=4):
    return (row * cols + col) * dtype_size
```

With `row` and `col` in the correct order, consecutive lanes address consecutive bytes in memory, and the 32-lane row read collapses down to just a few 32-byte transactions instead of 32.

---

### 🛡️ Production Prevention Invariants
1. **Access-Pattern Tests:** For any indexing formula meant to be contiguous across a warp, assert consecutive lane addresses differ by exactly `dtype_size`.
2. **Transaction-Count Regression:** Keep a small coalescing simulator as a standing test so an accidental row/column swap shows up as a transaction-count regression immediately.
3. **Profile Real Kernels:** Cross-check simulated transaction counts against a real profiler's global memory load efficiency metric before trusting a mental model of the access pattern.
