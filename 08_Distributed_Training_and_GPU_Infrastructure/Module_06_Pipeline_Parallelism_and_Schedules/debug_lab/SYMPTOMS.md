# Debug Lab Incident Report: 1F1B Schedule Makes the Last Pipeline Stage Idle Before Its First Backward Pass

- **Severity:** P2 Performance Regression (Pipeline Bubble Inflation)
- **Affected Subsystem:** Module_06_Pipeline_Parallelism_and_Schedules
- **Reported Impact:** A 1F1B (one-forward-one-backward) pipeline schedule generator computes, for a 4-stage pipeline running 8 microbatches, how many forward-only "warmup" microbatches each stage must process before it starts alternating forward and backward passes. The last stage -- which produces the loss and should be able to start its backward pass the instant its own forward pass completes -- is scheduled with a nonzero warmup count.

---

## 🚨 Observable Symptoms & Logs
```text
num_stages=4, num_microbatches=8
Warmup forward-pass count per stage (0..3): [4, 3, 2, 1]
Last stage (3) warmup count: 1 (expected: 0 -- the last stage produces the loss and should begin 1F1B immediately)
Total bubble steps across all stages: 10 (expected: 6)
```
Every stage's warmup count is one higher than it should be, and the total bubble overhead across all four stages (10) is 4 steps more than the textbook 1F1B bubble size for a 4-stage pipeline (6).

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_Pipeline_Parallelism_and_Schedules/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_1f1b_schedule.py
   ```
3. Compare the last stage's printed warmup count against the "(expected: 0 ...)" note, and the total bubble steps against the "(expected: ...)" note.

---

## 🎯 Your Objective
1. Inspect `broken_1f1b_schedule.py`'s `warmup_microbatch_count()` function and its `count = num_stages - stage_id` line.
2. Work out, for the very last stage (`stage_id = num_stages - 1`), what `num_stages - stage_id` evaluates to, and why the last stage of a 1F1B schedule should be able to start alternating forward/backward passes immediately with zero warmup.
3. Formulate a hypothesis for why every stage's warmup count -- not just the last stage's -- is off by exactly one, then check `ANSWERS.md`.
