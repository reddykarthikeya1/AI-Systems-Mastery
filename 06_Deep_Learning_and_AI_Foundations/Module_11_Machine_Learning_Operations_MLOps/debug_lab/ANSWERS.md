# Debug Lab Solution & Forensic Post-Mortem

## Incident: Same Feature Value Produces Different Predictions in Training vs Serving

---

### 🔍 Forensic Root Cause Analysis
`serve_request()` calls `compute_stats(request_batch)` to get the `mean`/`std` used for normalization, recomputing them from whatever happens to be in the *current serving batch* instead of reusing the `mean`/`std` that were computed once from the *training* data. A single-request batch of `[12.0]` has a standard deviation of exactly `0`, so `normalize()` falls back to returning `0.0` regardless of the input value, collapsing the serving-time prediction to just the model's bias term. This is a textbook train/serve skew bug: normalization statistics must be frozen at training time and shipped alongside the model, never recomputed from live traffic.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def serve_request(raw_feature, train_mean, train_std):
    normalized = normalize(raw_feature, train_mean, train_std)
    return predict(normalized)
```

Reusing the stored training-time `mean`/`std` at serving time makes the serving prediction identical to the training-time prediction for the same raw input, eliminating the skew.

---

### 🛡️ Production Prevention Invariants
1. **Persist Preprocessing Stats:** Save normalization statistics as part of the model artifact and load them at serving time; never recompute them from request traffic.
2. **Train/Serve Parity Tests:** Run a standing test that feeds the same example through the training-time and serving-time code paths and asserts identical outputs.
3. **Feature Store Discipline:** Route both training and serving through the same feature-transformation code path (e.g. a shared feature store) so they cannot drift apart.
