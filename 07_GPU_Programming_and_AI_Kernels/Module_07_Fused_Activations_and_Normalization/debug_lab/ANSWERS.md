# Debug Lab Solution & Forensic Post-Mortem

## Incident: Fused LayerNorm Under-Normalizes Off-Center Rows

---

### 🔍 Forensic Root Cause Analysis
`fused_layernorm()` sets `var = sum_x2 / n`, which is `E[X^2]`, not `Var(X)`. The single-pass "Welford-free" variance identity is `Var(X) = E[X^2] - (E[X])^2`; the kernel accumulates both `sum_x` and `sum_x2` in its one fused loop but only ever forms `E[X^2]` from `sum_x2`, dropping the `-(E[X])^2` correction term entirely. For the sample row (mean 12), `E[X^2]` is dominated by the squared mean itself (~144), so `var` comes out roughly two orders of magnitude too large, which makes `denom = sqrt(var + eps)` far too large and crushes every normalized output toward zero. When the row happens to be mean-centered around 0, `E[X]` is 0 and the missing term vanishes, which is exactly why this class of bug survives code review on "nice" test rows and only surfaces on real, off-center activations.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def fused_layernorm(x, eps=1e-5):
    n = len(x)
    sum_x = 0.0
    sum_x2 = 0.0
    for v in x:
        sum_x += v
        sum_x2 += v * v
    mean = sum_x / n
    var = sum_x2 / n - mean * mean  # E[X^2] - (E[X])^2
    denom = (var + eps) ** 0.5
    return [(v - mean) / denom for v in x]
```

---

### 🛡️ Production Prevention Invariants
1. **Never Test Only Mean-Zero Inputs:** Any single-pass variance kernel must be validated on rows with a non-trivial mean, since the missing-correction-term bug is invisible at mean 0.
2. **Cross-Check Against a Two-Pass Reference:** Keep a naive two-pass mean/variance implementation as a golden reference for fused statistics kernels; disagreement beyond floating-point tolerance is a hard fail.
3. **Guard Against Catastrophic Cancellation Too:** Even the corrected `E[X^2] - (E[X])^2` form loses precision when `mean` is large relative to the spread of `x`; prefer a shifted or Welford-style running variance for production kernels operating on real activation magnitudes.
