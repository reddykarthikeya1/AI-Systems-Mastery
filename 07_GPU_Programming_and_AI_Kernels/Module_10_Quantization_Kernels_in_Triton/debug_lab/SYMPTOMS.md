# Debug Lab Incident Report: INT8 Quantizer Clips Its Largest Activation to the Rail

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_10_Quantization_Kernels_in_Triton
- **Reported Impact:** A per-tensor INT8 quantization kernel is run on an 8-element activation row where seven values are small (roughly -0.2 to 0.2) and one is a large outlier (8.5). Round-tripping the tensor through `quantize_int8` -> `dequantize_int8` should reproduce every value closely; instead one element comes back wildly wrong while the rest look fine.

---

## 🚨 Observable Symptoms & Logs
```text
Original activations: [0.1, -0.2, 0.15, 0.05, -0.1, 8.5, 0.2, -0.05]
Per-tensor scale used: 0.009203
Quantized int8 levels: [11, -22, 16, 5, -11, 127, 22, -5]
Dequantized round-trip: [0.1012, -0.2025, 0.1472, 0.046, -0.1012, 1.1687, 0.2025, -0.046]
Per-element absolute error: [0.0012, 0.0025, 0.0028, 0.004, 0.0012, 7.3312, 0.0025, 0.004]
Max absolute error: 7.3312
```
The seven small values round-trip to within about 0.004 of their originals. The outlier (index 5, value `8.5`) round-trips to `1.1687` -- its quantized level is pinned at exactly `127`, the maximum representable INT8 level, and its dequantized value is off by more than 7.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_10_Quantization_Kernels_in_Triton/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_int8_quantize.py
   ```
3. Look at the quantized int8 levels list: notice one entry sits exactly at the maximum representable level (127) while the rest use only a small fraction of the available range.

---

## 🎯 Your Objective
1. Inspect `broken_int8_quantize.py`'s `compute_scale()` function and how its result is used to convert each float into an int8 level in `quantize_int8()`.
2. Work out what value `compute_scale()` computes from `activations`, and how that compares to the value that actually needs to map to the top of the int8 range (127) without clipping.
3. Formulate a hypothesis for why the seven small values are quantized with plenty of headroom to spare while the outlier saturates, then check `ANSWERS.md`.
