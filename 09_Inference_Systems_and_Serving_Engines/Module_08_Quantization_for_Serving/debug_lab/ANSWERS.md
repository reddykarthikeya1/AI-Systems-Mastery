# Debug Lab Solution & Forensic Post-Mortem

## Incident: INT8-Quantized Model Outputs Are Uniformly Biased

---

### Forensic Root Cause Analysis
`quantize()` correctly applies asymmetric quantization's two steps -- scale
and shift by `zero_point`:

```python
def quantize(values, scale, zero_point):
    return [... round(v / scale) + zero_point ...]
```

But `dequantize()` only undoes the scaling, not the shift:

```python
def dequantize(qvalues, scale, zero_point):
    return [q * scale for q in qvalues]
```

`zero_point` (73 here) is baked into every quantized code -- code `73`
represents real value `0.0`, code `109` represents real value `1.0`, and so
on. Multiplying the raw code by `scale` without first subtracting
`zero_point` reconstructs `code * scale` instead of
`(code - zero_point) * scale`, which is off by exactly `zero_point * scale`
(`73 * 0.0275 ≈ 2.0`) for every single value -- precisely the constant offset
observed. This is why symmetric quantization (`zero_point == 0`) can get away
with `dequantize(q) = q * scale`, but asymmetric quantization -- needed here
because the weight range `[-2.0, 5.0]` isn't centered on zero -- cannot.

---

### Production Corrective Action & Code Fix

```python
def dequantize(qvalues, scale, zero_point):
    return [(q - zero_point) * scale for q in qvalues]
```

With the fix, `dequantize(quantize(weights))` reconstructs values within
normal INT8 rounding error (a fraction of `scale`) of the originals instead
of being shifted by a constant `zero_point * scale`.

---

### Production Prevention Invariants
1. **Quantize/Dequantize Must Be Inverse Operations:** Any dequantization
   function must undo every transform its matching quantization function
   applied, in reverse order -- shift and scale are not optional based on
   which quantization scheme is in use.
2. **Round-Trip Test:** Unit test `dequantize(quantize(x)) ≈ x` for a range of
   values that is deliberately *not* symmetric around zero, since symmetric
   test data (e.g. `[-1, 0, 1]`) can hide a dropped zero-point.
3. **Constant-Offset Detection:** When comparing quantized vs. reference
   outputs, check whether the error is centered at zero (expected rounding
   noise) or shifted by a roughly constant amount (a strong signal of a
   missing zero-point term, not random rounding).
