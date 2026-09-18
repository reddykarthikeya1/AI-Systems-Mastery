# Debug Lab Incident Report: FP8 Block-Scaled Accumulation Collapses Toward Zero

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_09_FlashAttention_3_and_Hopper_Blackwell_Features
- **Reported Impact:** FA3's Hopper/Blackwell FP8 path quantizes each K/V tile with its own per-block scale (two-level scaling: block scale + an outer tensor scale) and accumulates the dequantized contributions into an fp32 output. Summing three small blocks that exactly sum to `[4.5, 4.0, 4.0, 2.0]` under exact arithmetic instead produces values roughly 30-50x smaller.

---

## 🚨 Observable Symptoms & Logs
```text
K/V blocks: [[1.0, -2.0, 3.0, 4.0], [0.5, 5.0, -1.5, 2.0], [3.0, 1.0, 2.5, -4.0]]
Reference (exact) sum:          [4.5, 4.0, 4.0, 2.0]
FP8 block-scaled accumulation:  [0.1461, 0.1651, 0.1137, 0.0791]
Entries off by more than 0.05: 4 of 4
```
FP8 quantization at 127 levels should track the exact sum to within a couple percent for values this size, not shrink every entry by more than an order of magnitude.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_09_FlashAttention_3_and_Hopper_Blackwell_Features/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_fp8_block_descale.py
   ```
3. Compare the reference sum against the FP8 block-scaled accumulation, entry by entry.

---

## 🎯 Your Objective
1. Inspect `broken_fp8_block_descale.py`'s `fp8_accumulate()` function and `dequantize_block()`.
2. Work out exactly how many times `block_scale` is applied to each quantized value between `dequantize_block()` and the loop in `fp8_accumulate()` that adds into `acc`.
3. Formulate a hypothesis for why the error scales with each block's own `block_scale` (small-magnitude blocks are hurt worse than large ones), then check `ANSWERS.md`.
