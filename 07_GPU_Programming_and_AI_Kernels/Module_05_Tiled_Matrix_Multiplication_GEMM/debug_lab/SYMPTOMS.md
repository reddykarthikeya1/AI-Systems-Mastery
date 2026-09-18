# Debug Lab Incident Report: Tiled Matmul Only Reflects the Last K-Tile's Partial Products

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_05_Tiled_Matrix_Multiplication_GEMM
- **Reported Impact:** A tiled GEMM implementation splits the reduction (K) dimension into tiles and is validated against a simple triple-loop reference matmul on a 4x4 x 4x4 product with `tile_size=2`, so there are two K-tiles to accumulate across. The tiled result disagrees with the reference on every single entry.

---

## 🚨 Observable Symptoms & Logs
```text
Tiled matmul (tile_size=2) vs triple-loop reference on a 4x4 x 4x4 product:
  row 0: reference=[20.0, 14.0, 8.0, 2.0]  tiled=[18.0, 13.0, 8.0, 3.0]
  row 1: reference=[30.0, 20.0, 10.0, 0.0]  tiled=[25.0, 18.0, 11.0, 4.0]
  row 2: reference=[40.0, 26.0, 12.0, -2.0]  tiled=[32.0, 23.0, 14.0, 5.0]
  row 3: reference=[50.0, 32.0, 14.0, -4.0]  tiled=[39.0, 28.0, 17.0, 6.0]
Mismatched entries: 15 of 16
```
The reference and tiled implementations multiply the exact same two matrices; a correct tiled implementation should produce identical results (zero mismatched entries), but every printed row shows the tiled values diverging from the reference values.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Tiled_Matrix_Multiplication_GEMM/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_tiled_matmul.py
   ```
3. Compare each row's 'reference=' values against its 'tiled=' values, and check the mismatch count.

---

## 🎯 Your Objective
1. Inspect `broken_tiled_matmul.py`'s `tiled_matmul()` function, specifically where `acc` is declared relative to the `t0` (K-tile) loop and where it is written into `c[i][j]`.
2. Work out how many K-tiles a 4x4 product with `tile_size=2` has, and what happens to `acc` between one K-tile and the next.
3. Formulate a hypothesis for why the tiled result is wrong on every entry, then check `ANSWERS.md`.
