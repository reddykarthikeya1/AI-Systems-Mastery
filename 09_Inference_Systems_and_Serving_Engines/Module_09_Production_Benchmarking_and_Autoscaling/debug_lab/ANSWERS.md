# Debug Lab Solution & Forensic Post-Mortem

## Incident: Autoscaler Never Scales Up During a Real Overload

---

### Forensic Root Cause Analysis
`record_tick()` computes its scaling signal as the average over the entire
history collected so far, not a recent window:

```python
self.history.append(utilization)
recent_avg = sum(self.history) / len(self.history)
```

`WINDOW_SIZE` is defined at module scope but never used. With 20 ticks of
`0.20` utilization already in `self.history` by the time the overload starts,
each new `0.95` sample is diluted by 20+ historical low-utilization samples:
after all 10 overload ticks, `recent_avg = (20*0.20 + 10*0.95) / 30 = 0.45`,
still well under the `0.80` threshold. The longer the healthy period before
an overload, the more diluted -- and the slower to detect -- any new
sustained spike becomes, which is exactly backwards for an autoscaler, whose
job is to react to *current* load.

---

### Production Corrective Action & Code Fix

```python
def record_tick(self, utilization, tick):
    self.history.append(utilization)
    recent_window = self.history[-WINDOW_SIZE:]
    recent_avg = sum(recent_window) / len(recent_window)
    if recent_avg > SCALE_UP_THRESHOLD:
        self.replicas += 1
        self.scale_events.append((tick, self.replicas, round(recent_avg, 3)))
```

Averaging only the last `WINDOW_SIZE` ticks means the moment the overload
starts, `recent_avg` climbs to `0.95` within `WINDOW_SIZE` ticks and crosses
`0.80`, triggering a scale-up around tick 20-22 instead of never.

---

### Production Prevention Invariants
1. **Sliding Window, Not Cumulative Average:** Any control-loop decision
   driven by "recent" load must use a bounded, recency-weighted window (fixed
   window, decay, or EWMA) -- an unbounded cumulative average is a
   correctness bug for control loops, not just an efficiency concern.
2. **Detect Unused Configuration:** A defined-but-unreferenced constant like
   `WINDOW_SIZE` is a strong static signal that the logic it was meant to
   gate was never wired in; lint or review for unused config values.
3. **Long-Running Simulation Test:** Autoscaler tests must include a long
   healthy period before an injected overload, not just an overload from
   tick zero -- cumulative-average bugs are invisible in short simulations
   where there's no history to dilute the signal.
