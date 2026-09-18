# Debug Lab Solution & Forensic Post-Mortem

## Incident: pass@k Benchmark Crashes With a ZeroDivisionError When k Exceeds the Number of Sampled Completions

---

### 🔍 Forensic Root Cause Analysis
The unbiased pass@k estimator implemented here,

```python
def pass_at_k(self, n, c, k):
    import math
    return 1.0 - (math.comb(n - c, k) / math.comb(n, k))
```

is only mathematically defined when `k <= n` -- you cannot choose `k` items out of a smaller pool of `n`. `math.comb(n, k)` does not raise for `k > n`; it returns `0`, since there are zero ways to choose more items than exist. `pass_at_k()` never checks that precondition before dividing, so as soon as a caller asks for pass@k with `k` greater than the number of samples actually generated for that problem -- an entirely ordinary situation, such as 5 completions sampled but a report configured for pass@10 -- the denominator `math.comb(n, k)` evaluates to `0` and the division raises `ZeroDivisionError`, taking down the whole benchmark run instead of just that one data point.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import math

class FixedBenchmark:
    def pass_at_k(self, n, c, k):
        if k > n:
            raise ValueError(f"k={k} exceeds n={n} sampled completions; sample more or lower k")
        if n - c < k:
            return 1.0   # comb(n - c, k) would be 0: every k-subset includes a passing sample
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))
```

Validating `k <= n` up front turns an opaque `ZeroDivisionError` into a clear, specific `ValueError` that names exactly what went wrong. The `n - c < k` short-circuit also handles the case where every remaining valid subset must contain at least one passing sample, returning the mathematically correct `1.0` directly instead of relying on `comb()` returning `0` implicitly.

---

### 🛡️ Production Prevention Invariants
1. **Validate Combinatorial Preconditions Before Evaluating Them:** Check `k <= n` explicitly and fail with a clear, specific error rather than letting a bare arithmetic exception surface from deep inside the formula.
2. **Isolate Failures Per-k in a Sweep:** A benchmark run across multiple k values should catch and log a failure for one k value rather than let it abort the entire run.
3. **Assert Sampling Budget Covers the Requested k Values at Config Time:** Require `n >= max(k_values)` when the sweep is configured, so this is caught before the run starts, not partway through a nightly job.
