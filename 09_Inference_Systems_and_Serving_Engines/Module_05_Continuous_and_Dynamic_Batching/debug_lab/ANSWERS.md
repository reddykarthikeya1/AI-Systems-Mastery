# Debug Lab Solution & Forensic Post-Mortem

## Incident: "Continuous" Batching Scheduler Runs No Faster Than Static Batching

---

### Forensic Root Cause Analysis
The admission check only fires when the batch is completely empty:

```python
if len(running) == 0:
    while waiting and len(running) < MAX_BATCH_SIZE:
        running.append(waiting.pop(0))
```

When `req_1` finishes at step 2, `req_2`, `req_3`, and `req_4` are still
running, so `len(running) == 3`, not `0`. The `if` guard is false, so
`waiting` is never even consulted -- the freed slot sits idle for the rest of
`req_4`'s 5 steps. Only once every request in the *original* batch has
finished simultaneously does `len(running)` reach `0` and the next wave get
admitted. This is exactly static (batch-of-batches) scheduling wearing a
continuous-batching label: it recreates the "wait for the whole batch to
drain" behavior continuous batching exists to eliminate.

---

### Production Corrective Action & Code Fix

```python
while waiting or running:
    step += 1
    # Continuous batching: backfill every freed slot immediately, regardless
    # of how many other requests are still running.
    while waiting and len(running) < MAX_BATCH_SIZE:
        running.append(waiting.pop(0))

    still_running = []
    for req in running:
        req.remaining -= 1
        if req.remaining <= 0:
            finished_at_step[req.name] = step
        else:
            still_running.append(req)
    running = still_running
```

Dropping the `if len(running) == 0:` guard and admitting whenever
`len(running) < MAX_BATCH_SIZE` lets `req_5` backfill `req_1`'s slot the
moment it frees at step 2, so `req_5`/`req_6` finish around step 4 and the
whole run completes in 5 steps instead of 7.

---

### Production Prevention Invariants
1. **Admission Trigger, Not Admission Window:** A continuous-batching
   scheduler's admission check must run every step against current free
   capacity (`len(running) < MAX_BATCH_SIZE`), never gated on the batch being
   fully empty -- that gate silently reintroduces static batching.
2. **Utilization Regression Test:** Track idle-slot-steps (free capacity
   while requests wait) across a scheduler run and assert it stays near zero
   whenever the waiting queue is non-empty.
3. **Mixed-Length Workload Coverage:** Test batching schedulers with requests
   of staggered lengths, not just uniform ones -- bugs like this are invisible
   when every request in a batch happens to finish at the same step.
