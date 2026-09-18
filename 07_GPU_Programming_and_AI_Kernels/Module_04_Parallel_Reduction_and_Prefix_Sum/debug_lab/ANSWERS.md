# Debug Lab Solution & Forensic Post-Mortem

## Incident: Parallel Tree Reduction Returns the Wrong Total for Non-Power-of-2 Input

---

### 🔍 Forensic Root Cause Analysis
The inner loop's stopping condition `i + stride < n` (strictly less than) causes the reduction to silently skip a pairing whenever `i + stride` lands exactly on the last valid index. For `n=6`: at `stride=1` the pairs `(0,1)`, `(2,3)`, `(4,5)` should all combine, but `i=4` gives `i + stride = 5`, which is `< 6`, so that pair *is* included there; the real gap appears at `stride=2`: `i=0` combines indices `(0,2)`, and the next candidate `i=4` gives `i + stride = 6`, which fails `6 < 6` and is skipped entirely -- so `buf[4]` (already holding the partial sum of original indices 4 and 5) never gets folded into `buf[0]`. For array sizes that aren't a power of two, this kind of strict boundary check drops whichever partial sum lands exactly at the array's edge on a given stride.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def tree_reduce_sum(values):
    buf = list(values)
    n = len(buf)
    stride = 1
    while stride < n:
        i = 0
        while i < n:
            if i + stride < n:
                buf[i] += buf[i + stride]
            i += stride * 2
        stride *= 2
    return buf[0]
```

Iterating `i` across the full range and only adding when a valid partner exists (rather than using the partner's existence as the loop's stopping condition) ensures every element's partial sum eventually reaches `buf[0]`, matching the reference `sum(data)` for any array length.

---

### 🛡️ Production Prevention Invariants
1. **Non-Power-of-2 Test Cases:** Always test reduction kernels against sizes that are *not* a power of two, not just convenient round numbers.
2. **Reference Comparison in Tests:** Compare any custom reduction against the language's built-in `sum()` (or equivalent) as a standing correctness test.
3. **Trace Boundary Strides by Hand:** For any doubling-stride algorithm, manually trace the last stride against odd/uneven array lengths before trusting the loop bounds.
