# Debug Lab Incident Report: Contiguous-Looking Row Read Triggers One Memory Transaction Per Lane

- **Severity:** P2 Memory Bandwidth Efficiency
- **Affected Subsystem:** Module_03_CUDA_Memory_Hierarchy_and_Coalescing
- **Reported Impact:** A warp of 32 threads is meant to read one contiguous row (32 consecutive float32 values) from a row-major matrix -- the textbook fully-coalesced access pattern that should need only a few 32-byte memory transactions. Instead the simulator reports needing one full transaction per thread.

---

## 🚨 Observable Symptoms & Logs
```text
Warp of 32 threads reading row 0 of a 32x32 row-major float32 matrix.
Byte addresses touched by lanes 0-7: [0, 128, 256, 384, 512, 640, 768, 896]
Memory transactions required: 32 (32-byte segments touched: [0, 4, 8, 12, 16, 20, 24, 28]...)
Ideal contiguous 32-lane row read should need only a handful of transactions, not 32.
```
Reading a single contiguous row of 32 floats (128 bytes) should need roughly 4 transactions of 32 bytes each, not 32.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_CUDA_Memory_Hierarchy_and_Coalescing/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_coalescing.py
   ```
3. Compare the reported transaction count to the 32 lanes being read.

---

## 🎯 Your Objective
1. Inspect `broken_coalescing.py`'s `compute_address()` function.
2. Work out which matrix index (`row` or `col`) actually varies as `lane` increases from 0 to 31 in `warp_access_pattern()`.
3. Formulate a hypothesis for why the access pattern isn't actually contiguous, then check `ANSWERS.md`.
