# Debug Lab Incident Report: INT8-Quantized Model Outputs Are Uniformly Biased

- **Severity:** P1 Accuracy Regression
- **Affected Subsystem:** Module_08_Quantization_for_Serving
- **Reported Impact:** After switching a serving deployment to INT8 weight
  quantization, model outputs shifted by a consistent, layer-dependent
  offset instead of the small symmetric rounding noise quantization is
  expected to introduce.

---

## Observable Symptoms & Logs
```text
Original FP32 weights: [-2.0, -1.0, 0.0, 1.0, 5.0]
scale=0.0275, zero_point=73
Quantized INT8 codes:  [0, 37, 73, 109, 255]
Expected dequantized weights (should closely match the originals): [-2.0, -1.0, 0.0, 1.0, 5.0]
Actual dequantized weights: [0.0, 1.0157, 2.0039, 2.9922, 7.0]
Per-element error (actual - expected): [2.0, 2.0157, 2.0039, 1.9922, 2.0]
```
Every single dequantized weight is off from the original by almost exactly
`+2.0`, not by small independent rounding noise. The error is a constant
shift, not quantization noise.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_Quantization_for_Serving/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_int8_quantizer.py
   ```
3. Observe that the per-element error column is nearly constant across all
   five weights instead of being small and centered near zero.

---

## Your Objective
1. Inspect `quantize()` and `dequantize()` and write out, by hand, the exact
   arithmetic each one performs on a single value.
2. Compare that against `compute_scale_and_zero_point()`, which computes both
   `scale` and `zero_point` for asymmetric quantization.
3. Formulate a hypothesis for why the error is a constant offset rather than
   noise, then check `ANSWERS.md`.
