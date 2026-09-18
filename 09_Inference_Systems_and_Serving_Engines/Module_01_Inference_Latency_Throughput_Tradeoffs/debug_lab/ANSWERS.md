# Debug Lab Solution & Forensic Post-Mortem

## Incident: Latency Dashboard Shows Flat 10ms p99 Under Static Batching

---

### Forensic Root Cause Analysis
`per_request_latency()` ignores the `completion_times` the simulator already
computed and instead returns each request's own `service_time` unchanged:

```python
def per_request_latency(request_service_times, completion_times):
    return [service_time for service_time in request_service_times]
```

It never uses `completion_times` at all. The simulator correctly models that a
static batch only starts once `batch_size` requests have queued, so the first
request in a batch of 4 actually waits through 3 batchmates plus its own
service time before it completes -- but the reporting function throws that
information away and substitutes the per-request GPU service time instead.
End-to-end latency (queueing delay + service time) is exactly the gap between
throughput-oriented batching and single-request latency, and this function
silently collapses that gap to zero.

---

### Production Corrective Action & Code Fix

```python
def per_request_latency(request_service_times, completion_times):
    # Latency is wall-clock time from arrival to completion. Requests arrive
    # one per tick (index i arrives at time i), so subtract arrival time from
    # the batch's completion time.
    return [
        completion - arrival
        for arrival, completion in enumerate(completion_times)
    ]
```

With the fix, the first request in each 4-request batch reports ~40ms (it
waits for the batch to fill and then for the full batch service time), the
last request in the batch reports ~10ms, and p99 correctly reflects the worst
case instead of matching the best case.

---

### Production Prevention Invariants
1. **Measure at the Boundary:** Latency must always be arrival-to-completion
   wall-clock time, never a proxy like per-request service time -- the two
   only agree when there is no queueing, which defeats the point of measuring
   latency under load.
2. **Batching Tradeoff Tests:** Any batching simulator should assert that p99
   latency strictly increases with batch size for a fixed arrival rate, since
   larger batches trade tail latency for throughput.
3. **Cross-Check Dashboards Against Ground Truth:** When a latency metric
   disagrees with user-reported experience, treat the metric's computation as
   suspect before treating the complaint as noise.
