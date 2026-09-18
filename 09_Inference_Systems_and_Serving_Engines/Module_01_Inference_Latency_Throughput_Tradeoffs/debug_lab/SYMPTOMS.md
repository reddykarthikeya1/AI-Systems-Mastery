# Debug Lab Incident Report: Latency Dashboard Shows Flat 10ms p99 Under Static Batching

- **Severity:** P2 Observability Gap
- **Affected Subsystem:** Module_01_Inference_Latency_Throughput_Tradeoffs
- **Reported Impact:** On-call was paged by users complaining requests "feel slow"
  under load, but the latency dashboard shows every request finishing in a flat
  10ms, identical to the single-request, unbatched case. The dashboard and the
  user complaints disagree.

---

## Observable Symptoms & Logs
```text
Reported per-request latency for a 4-request static batch, service=10ms each:
reported: p50=10.00ms p99=10.00ms avg=10.00ms
Expected: the last request in each batch should show ~40.00ms end-to-end latency
(it waits for 3 batchmates before the batch even starts).
Actual reported p99 latency: 10.00ms
```
Every request reports exactly 10ms regardless of its position in the batch, even
though the simulator models a batch that only starts running once 4 requests have
queued up.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_Inference_Latency_Throughput_Tradeoffs/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_latency_report.py
   ```
3. Observe that reported p50/p99/avg latency never rises above the per-request
   GPU service time, no matter the batch size.

---

## Your Objective
1. Inspect `broken_latency_report.py`, especially `per_request_latency()`, and
   trace what value it actually returns for each request.
2. Compare that against what "end-to-end latency" should mean for a request
   sitting in a static batch queue.
3. Formulate a hypothesis for why queueing delay never shows up in the report,
   then check `ANSWERS.md`.
