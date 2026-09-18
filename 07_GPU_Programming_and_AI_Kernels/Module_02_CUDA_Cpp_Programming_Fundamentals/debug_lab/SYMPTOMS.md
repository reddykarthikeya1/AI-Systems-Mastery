# Debug Lab Incident Report: Kernel Launch Leaves Most Output Elements Unwritten

- **Severity:** P1 Correctness / Coverage
- **Affected Subsystem:** Module_02_CUDA_Cpp_Programming_Fundamentals
- **Reported Impact:** A simple element-wise kernel is launched with 4 blocks of 8 threads each to fully populate a 32-element output array, one element per thread. After the kernel 'runs', a large majority of the output array is still `None` (never written), while several elements were overwritten many times.

---

## 🚨 Observable Symptoms & Logs
```text
Kernel launched with 4 blocks x 8 threads for 32 output elements.
Output array: [0, 8, 16, 24, 25, 26, 27, 28, 29, 30, 31, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
Elements never written by any thread: 21 of 32 -> indices [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
```
With 4 blocks x 8 threads = 32 total threads for 32 output elements, a correctly indexed kernel should leave zero elements untouched.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_CUDA_Cpp_Programming_Fundamentals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_global_index.py
   ```
3. Check how many output indices are still `None` after the kernel 'runs'.

---

## 🎯 Your Objective
1. Inspect `broken_global_index.py`'s `compute_global_index()` function.
2. Work out the full range of index values it can actually produce for `num_blocks=4`, `block_dim=8`.
3. Formulate a hypothesis for why most of the array is untouched, then check `ANSWERS.md`.
