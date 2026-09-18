# Debug Lab Solution & Forensic Post-Mortem

## Incident: INT8 Quantizer Clips Its Largest Activation to the Rail

---

### 🔍 Forensic Root Cause Analysis
`compute_scale()` derives the per-tensor scale from the *mean* absolute value (`avg_abs = sum(abs(v) for v in tensor) / len(tensor)`), not the *maximum* absolute value. For a symmetric int8 quantizer, the scale must map the single largest-magnitude element in the tensor to the edge of the representable range (`qmax = 127`) exactly: `scale = max(abs(x)) / qmax`. Using the mean instead produces a scale that is far too small whenever the tensor has even one outlier pulling the mean away from where most of the mass sits (here the mean absolute value is dragged up only slightly by the single 8.5, while the other seven values are all under 0.2). Every value is quantized as `round(v / scale)`, and because `scale` is too small, `v / scale` overshoots the representable range for the outlier and gets clamped at `qmax`. The seven small values, meanwhile, are quantized far too coarsely relative to their own magnitude (large quantization step, most of the int8 range unused by them) -- the classic signature of computing a clipping-based scale from the mean: outliers saturate while everything else loses precision it didn't need to lose.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def compute_scale(tensor, qmax=127):
    max_abs = max(abs(v) for v in tensor)
    return max_abs / qmax
```

---

### 🛡️ Production Prevention Invariants
1. **Scale From the Extremum, Not the Average:** A symmetric min-max (or absmax) quantizer's scale must be derived from `max(abs(x))` so the largest-magnitude value maps to exactly the top representable level; a mean-based scale guarantees clipping on any outlier-bearing tensor.
2. **Test With an Outlier Present:** Always include at least one deliberately large-magnitude value in quantization unit tests; an all-similar-magnitude test tensor can hide a mean-vs-max scale bug indefinitely.
3. **Track Saturation Rate in Production:** Monitor the fraction of quantized values landing exactly at `+qmax`/`-qmax-1`; a nonzero, growing saturation rate on real activations is a strong signal the scale is being computed incorrectly (or that per-channel/per-block scaling is needed instead of per-tensor).
