# Debug Lab Incident Report: Autoscaler Never Scales Up During a Real Overload

- **Severity:** P1 Availability Risk
- **Affected Subsystem:** Module_09_Production_Benchmarking_and_Autoscaling
- **Reported Impact:** During a sustained traffic surge, replica count stayed
  flat at its floor even though utilization had clearly crossed the scale-up
  threshold for many consecutive ticks, leading to request queueing and
  latency SLO breaches that paging alerts on utilization alone never caught.

---

## Observable Symptoms & Logs
```text
Simulated 30 ticks: 20 healthy ticks at util=0.20, then 10 overloaded ticks
at util=0.95 (threshold=0.8).
Expected: the autoscaler should scale up within a few ticks of the overload
starting (around tick 20-22), since recent utilization is well above
threshold.
Actual scale-up events (tick, replicas, avg_used): []
Final replica count after the full 30-tick simulation: 2
```
Ten consecutive ticks run at 95% utilization -- nearly 4x the 20% baseline
and well above the 80% scale-up threshold -- yet `scale_events` is empty and
`replicas` never moves off its starting value of 2.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_09_Production_Benchmarking_and_Autoscaling/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_autoscaler.py
   ```
3. Observe that `record_tick()` never triggers a scale-up even during the
   last 10 ticks, all pinned well above `SCALE_UP_THRESHOLD`.

---

## Your Objective
1. Inspect `Autoscaler.record_tick()` and work out exactly what `recent_avg`
   is averaged over as the simulation progresses.
2. Compare that against `WINDOW_SIZE`, which is defined but never referenced
   anywhere in the class.
3. Formulate a hypothesis for why 10 ticks of sustained 95% utilization fail
   to push the average over 80%, then check `ANSWERS.md`.
