# Debug Lab Solution & Forensic Post-Mortem

## Incident: Attention Weights Do Not Sum to One

---

### Forensic Root Cause Analysis
`softmax_over_scores()` computes `col_sums`, the sum of `exp(score)` down each
*column* of the scores matrix (i.e. summed across queries, for a fixed key), and then
divides every entry by its column's sum. A per-query softmax must instead normalize
each *row* -- summing across keys for a fixed query -- so that the weights a single
query assigns to all the keys add up to 1.0. Normalizing over the wrong axis means
each token's attention distribution is scaled by an unrelated quantity (how much
total attention that key received from every query), so the row sums drift away from
1.0 in whichever direction that column happens to be over- or under-weighted.

---

### Production Corrective Action & Code Fix

```python
def softmax_over_scores(scores):
    exps = [[math.exp(v) for v in row] for row in scores]
    row_sums = [sum(row) for row in exps]
    return [[val / row_sums[r] for val in exps[r]] for r in range(len(exps))]
```

With normalization moved to the row axis, every query's attention weights sum to
exactly `1.000`, as required for a valid probability distribution.

---

### Production Prevention Invariants
1. **Invariant Assertion:** Assert `abs(sum(row) - 1.0) < 1e-6` for every row of any
   softmax output in tests.
2. **Axis Documentation:** Explicitly name which axis a normalization reduces over in
   the variable name (`row_sums` vs `col_sums`) so a mismatch is visible on read.
3. **Small Hand-Checkable Fixtures:** Keep a tiny 3x3 attention fixture with
   hand-computed expected weights as a permanent regression test.
