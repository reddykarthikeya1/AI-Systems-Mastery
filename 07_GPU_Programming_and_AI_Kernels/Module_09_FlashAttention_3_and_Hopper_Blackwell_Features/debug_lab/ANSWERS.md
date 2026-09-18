# Debug Lab Solution & Forensic Post-Mortem

## Incident: FP8 Block-Scaled Accumulation Collapses Toward Zero

---

### 🔍 Forensic Root Cause Analysis
`dequantize_block(q, block_scale)` already multiplies every quantized level `q[i]` by `block_scale` to return real-valued numbers (`v = q[i] * block_scale`). But the accumulation loop in `fp8_accumulate()` does `acc[i] += v * block_scale` -- multiplying by `block_scale` a *second* time on values that were already dequantized. Each block's contribution to `acc` therefore ends up scaled by `block_scale ** 2` instead of `block_scale ** 1`. Because `block_scale = max(abs(block)) / 127` is itself a small number (well under 1 for these inputs), squaring it makes the error compound: blocks with a smaller max magnitude (and hence a smaller `block_scale`) are shrunk far more than blocks with a larger one, so the distortion is not a uniform multiplicative factor across blocks, and no single global correction after the fact can fix it. This is the FP8-scaling analogue of double-dividing by the same normalization factor twice.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def fp8_accumulate(blocks, tensor_scale=1.0):
    width = len(blocks[0])
    acc = [0.0] * width
    for block in blocks:
        q, block_scale = quantize_block(block)
        dequantized = dequantize_block(q, block_scale)  # already real-valued
        for i, v in enumerate(dequantized):
            acc[i] += v  # do not re-multiply by block_scale
    return [v * tensor_scale for v in acc]
```

---

### 🛡️ Production Prevention Invariants
1. **One Scale, One Application:** Every quantize/dequantize pair should have exactly one place in the code where the scale is applied on the way out; document it at that single call site so a second, redundant multiply cannot creep in nearby.
2. **Round-Trip Test Each Block in Isolation:** Before wiring blocks into a multi-block accumulator, assert `dequantize_block(*quantize_block(block)) ~= block` for each block on its own, which would have caught this the moment `fp8_accumulate` was integrated.
3. **Watch for Magnitude-Dependent Error:** A bug that scales with input magnitude (rather than a fixed percentage error) is a strong signal that a scale factor is being applied the wrong number of times, not that quantization precision is simply too low.
