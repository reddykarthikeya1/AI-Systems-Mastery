# Debug Lab Solution & Forensic Post-Mortem

## Incident: Held-Out Accuracy Is Implausibly High

---

### Forensic Root Cause Analysis
`train_test_split` shuffles the dataset indices and correctly slices out
`train_idx = indices[:split]`. But instead of letting `test_idx` be the remaining
`indices[split:]`, it draws a **fresh, independent random sample** of `n - split`
indices from the *entire* index range with `random.Random(seed + 1).sample(range(n), ...)`.
Because that sample is drawn from all `n` indices rather than only the held-out
remainder, a large fraction of the "test" indices also land inside `train_idx` by
chance. The memorizing model has exact answers for those overlapping points, so
accuracy is inflated well above the majority-class baseline -- a textbook case of
train/test data leakage.

---

### Production Corrective Action & Code Fix

```python
def train_test_split(data, labels, train_frac=0.8, seed=42):
    n = len(data)
    indices = list(range(n))
    random.Random(seed).shuffle(indices)
    split = int(n * train_frac)
    train_idx = indices[:split]
    test_idx = indices[split:]  # the held-out remainder, not a fresh sample
    ...
```

With the fix, `overlap` is always the empty set and the reported accuracy tracks the
majority-class baseline, as expected for data with no learnable signal.

---

### Production Prevention Invariants
1. **Assert Disjointness:** Any split function should assert
   `set(train_idx).isdisjoint(test_idx)` before returning.
2. **Leakage Canary:** Track "indices in both sets" as a first-class metric in the
   evaluation pipeline, alerting when it is ever nonzero.
3. **Suspicious-Result Review:** Treat evaluation numbers that beat a sanity baseline
   by a wide margin as a leakage signal to investigate, not a result to celebrate.
