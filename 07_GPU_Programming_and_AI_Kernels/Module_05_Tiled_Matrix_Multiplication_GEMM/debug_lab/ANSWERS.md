# Debug Lab Solution & Forensic Post-Mortem

## Incident: Tiled Matmul Only Reflects the Last K-Tile's Partial Products

---

### 🔍 Forensic Root Cause Analysis
`acc` is declared *inside* the `t0` loop (`for t0 in range(0, k, tile_size)`), so it is reset to `0.0` at the start of every K-tile, and `c[i][j] = acc` overwrites (rather than accumulates into) the output on every K-tile too. With `k=4` and `tile_size=2` there are two K-tiles per output element, but because `acc` never persists across them, only the *second* K-tile's partial dot product ever survives into `c[i][j]` -- the first K-tile's contribution is computed and then thrown away. A correct tiled reduction must accumulate the running partial sum for `c[i][j]` across *all* K-tiles, initializing it once before the K-tile loop begins and adding into it (not overwriting it) on every K-tile.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def tiled_matmul(a, b, tile_size):
    n, k, m = len(a), len(b), len(b[0])
    c = [[0.0] * m for _ in range(n)]
    for i0 in range(0, n, tile_size):
        for j0 in range(0, m, tile_size):
            for t0 in range(0, k, tile_size):
                for i in range(i0, i0 + tile_size):
                    for j in range(j0, j0 + tile_size):
                        for t in range(t0, t0 + tile_size):
                            c[i][j] += a[i][t] * b[t][j]   # accumulate across K-tiles
    return c
```

Accumulating directly into `c[i][j]` across every K-tile (instead of resetting a local `acc` each K-tile and overwriting the output) makes the tiled result match the triple-loop reference exactly, with zero mismatched entries.

---

### 🛡️ Production Prevention Invariants
1. **K-Tile Accumulation Tests:** Always test tiled GEMM against a K dimension split into 2 or more tiles, not just a single K-tile that hides an accumulation bug.
2. **Reference-Diff in CI:** Run tiled implementations against a naive reference for small shapes as a standing correctness gate.
3. **Accumulator Scope Review:** Treat the scope of any reduction accumulator as safety-critical -- it must be initialized once outside the reduction loop and only ever added into inside it.
