# Debug Lab Incident Report: Triton-Style Vector-Add Kernel Produces Overlapping, Incorrect Blocks

- **Severity:** P1 Correctness / Block Partitioning
- **Affected Subsystem:** Module_06_OpenAI_Triton_Programming_Fundamentals
- **Reported Impact:** A Triton-style vector-add kernel partitions a 12-element array into blocks of 4 elements each (`pid=0,1,2`) and writes `a[i] + b[i]` into each block's slice of the output. Several output positions come out wrong, and not just at the array boundary.

---

## 🚨 Observable Symptoms & Logs
```text
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
b = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
kernel output   = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, None, None]
expected output = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122]
mismatched positions: [10, 11]
```
Every position should satisfy `kernel output[i] == a[i] + b[i]`, but the mismatch list is not empty.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_OpenAI_Triton_Programming_Fundamentals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_block_partition.py
   ```
3. Check the 'mismatched positions' list against an all-correct run, which should print an empty list.

---

## 🎯 Your Objective
1. Inspect `broken_block_partition.py`'s `vector_add_kernel()` function, specifically how `block_start` is derived from `pid`.
2. Work out which array index each `(pid, offset)` pair actually writes to for `pid=0`, `pid=1`, and `pid=2`.
3. Formulate a hypothesis for the overlapping/incorrect writes, then check `ANSWERS.md`.
