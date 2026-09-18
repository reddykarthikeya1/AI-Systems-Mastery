# Debug Lab Incident Report: DDP Effective Gradient Scales Up With Accumulation Steps

- **Severity:** P1 Training Instability
- **Affected Subsystem:** Module_03_Distributed_Data_Parallel_DDP
- **Reported Impact:** Two DDP ranks each run 4 microbatches of gradient accumulation before the usual cross-rank gradient sync. Every microbatch on every rank happens to produce the exact same gradient `[1.0, 2.0]`, so the true effective per-step gradient a well-behaved optimizer should see is also `[1.0, 2.0]`. The pipeline instead hands the optimizer a gradient 4x that size.

---

## 🚨 Observable Symptoms & Logs
```text
world_size=2, accumulation_steps=4
Single-microbatch gradient (reference): [1.0, 2.0]
DDP step's effective gradient:           [4.0, 8.0]
Ratio to reference: [4.0, 4.0]
```
Changing `accumulation_steps` changes this ratio in lockstep: doubling `accumulation_steps` doubles the effective gradient's magnitude relative to any single microbatch's gradient, even though `world_size` and every microbatch's own gradient stay fixed.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_Distributed_Data_Parallel_DDP/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_ddp_grad_accum.py
   ```
3. Compare the "DDP step's effective gradient" line against the "Single-microbatch gradient (reference)" line and the printed ratio.

---

## 🎯 Your Objective
1. Inspect `broken_ddp_grad_accum.py`'s `local_accumulated_grad()` function and work out what it does to `accumulation_steps` separate microbatch gradients before the cross-rank sync ever happens.
2. Inspect `allreduce_average()` and confirm exactly what normalization it applies, and across what dimension (ranks, or microbatches, or both).
3. Formulate a hypothesis for why the ratio observed matches `accumulation_steps` rather than `world_size` or some other constant, then check `ANSWERS.md`.
