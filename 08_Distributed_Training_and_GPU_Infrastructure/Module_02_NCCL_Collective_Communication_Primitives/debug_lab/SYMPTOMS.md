# Debug Lab Incident Report: Ring All-Reduce Mean Gradient Is 4x Too Small

- **Severity:** P1 Numerical Correctness (Silent Training Degradation)
- **Affected Subsystem:** Module_02_NCCL_Collective_Communication_Primitives
- **Reported Impact:** A ring all-reduce simulation combines four ranks' per-parameter gradients via reduce-scatter followed by a final averaging step. The output gradient used for the optimizer step is far smaller than the true mean of the four ranks' gradients -- by a factor that lines up suspiciously with `world_size`.

---

## 🚨 Observable Symptoms & Logs
```text
world_size=4, per-rank gradients: [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0], [3.0, 4.0, 5.0], [4.0, 5.0, 6.0]]
Expected all-reduced mean gradient: [2.5, 3.5, 4.5]
ring_allreduce_mean() output:       [0.625, 0.875, 1.125]
Ratio actual/expected on element 0: 0.2500 (should be 1.0)
```
`ring_allreduce_mean()` is supposed to return the elementwise mean of the four ranks' gradients. The reported values are exactly `1/world_size` (0.25 = 1/4) times the correct mean on every element, not merely "off" by some rounding error.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_NCCL_Collective_Communication_Primitives/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_ring_allreduce.py
   ```
3. Compare the "Expected all-reduced mean gradient" line against the `ring_allreduce_mean()` output line, and note the printed ratio.

---

## 🎯 Your Objective
1. Inspect `broken_ring_allreduce.py`'s `reduce_scatter_sum()` function and work out exactly what value it returns for each chunk -- a sum across ranks, or something already divided by `world_size`.
2. Then inspect `ring_allreduce_mean()` and see what it does to the value returned by `reduce_scatter_sum()`.
3. Formulate a hypothesis for why the final ratio is exactly `1/world_size` rather than some arbitrary error, then check `ANSWERS.md`.
