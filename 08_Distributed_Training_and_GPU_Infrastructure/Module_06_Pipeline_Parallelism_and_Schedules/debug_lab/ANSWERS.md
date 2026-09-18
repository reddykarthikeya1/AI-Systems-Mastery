# Debug Lab Solution & Forensic Post-Mortem

## Incident: 1F1B Schedule Makes the Last Pipeline Stage Idle Before Its First Backward Pass

---

### 🔍 Forensic Root Cause Analysis
In the standard 1F1B (PipeDream-Flush) schedule, stage `s` (0-indexed, `s = 0` is the first stage nearest the input) must run `num_stages - 1 - s` forward-only warmup microbatches before its backward pass for the first microbatch becomes available, because that microbatch's activation has to travel through all `num_stages - 1` *remaining* downstream stages and its gradient has to travel all the way back before stage `s` can consume it. The last stage (`s = num_stages - 1`) is the one exception: it computes the loss directly from its own forward output, so its backward pass for microbatch 0 is available immediately after its own forward pass -- its warmup count must be exactly 0. `warmup_microbatch_count()` computes `count = num_stages - stage_id`, which is uniformly one larger than the correct `num_stages - 1 - stage_id` for every stage, so the last stage gets a warmup count of 1 instead of 0: it sits idle for one full extra forward-pass slot before it can start any backward work, and the same off-by-one inflates every other stage's warmup phase too. Summed across all stages, this adds `num_stages` extra idle steps to the pipeline's total bubble overhead on every training step (10 vs. the correct 6 here), which compounds over the life of a long training run.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def warmup_microbatch_count(stage_id, num_stages, num_microbatches):
    count = num_stages - 1 - stage_id  # last stage (stage_id = num_stages - 1) gets 0
    return min(count, num_microbatches)
```

---

### 🛡️ Production Prevention Invariants
1. **Anchor the Formula at the Boundary Stage:** Any per-stage pipeline-schedule formula should be checked first at `stage_id = num_stages - 1` (and `stage_id = 0`), where the correct value is a well-known constant (0 warmup for the last stage) -- off-by-one errors are far easier to spot at the boundary than in the middle of the range.
2. **Cross-Check the Total Bubble Against the Closed-Form Formula:** The 1F1B bubble size has a known closed form (`num_stages - 1` steps' worth of pipeline fill, summed appropriately across stages); any schedule generator should assert its total idle-step count matches that formula for a range of `num_stages`/`num_microbatches` combinations.
3. **Visualize the Schedule, Don't Just Trust the Counts:** Render the full per-stage timeline (which microbatch each stage processes forward/backward on each clock step) for a small pipeline in tests; an inflated bubble is immediately visible as a stage sitting idle in the timeline when it should already have work queued.
