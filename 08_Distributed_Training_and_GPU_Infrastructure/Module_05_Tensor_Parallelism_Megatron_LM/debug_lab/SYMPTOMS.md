# Debug Lab Incident Report: Row-Parallel Linear Layer Output Is Half the Reference Value

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_05_Tensor_Parallelism_Megatron_LM
- **Reported Impact:** A row-parallel linear layer shards its input features and matching weight rows across 2 tensor-parallel ranks, has each rank compute a partial sum over its own shard of the reduction dimension, and then combines the two ranks' partial outputs. The combined output disagrees with a plain, un-sharded reference implementation of the same linear layer on the same input and weights.

---

## 🚨 Observable Symptoms & Logs
```text
tp_size=2, per-rank partial outputs: [[5.0, 2.5], [5.5, 12.5]]
Un-sharded reference output: [10.5, 15.0]
Row-parallel combined output: [5.25, 7.5]
```
Element-wise, `10.5 / 5.25 = 2.0` and `15.0 / 7.5 = 2.0` -- the combined output is exactly half the reference output, and that factor of 2 matches `tp_size`.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Tensor_Parallelism_Megatron_LM/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_row_parallel_linear.py
   ```
3. Compare the "Un-sharded reference output" line against the "Row-parallel combined output" line, and check the per-rank partial outputs printed above them.

---

## 🎯 Your Objective
1. Inspect `broken_row_parallel_linear.py`'s `row_parallel_partial()` function: each rank computes a partial sum over *its own shard* of the reduction (input-feature) dimension. Work out what mathematical operation must combine those partial sums to reconstruct the full un-sharded sum over the complete reduction dimension.
2. Inspect `row_parallel_combine()` and see what operation it actually performs across ranks.
3. Formulate a hypothesis for why the discrepancy factor is exactly `tp_size`, then check `ANSWERS.md`.
