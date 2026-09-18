# Debug Lab Incident Report: "Continuous" Batching Scheduler Runs No Faster Than Static Batching

- **Severity:** P2 Throughput Regression
- **Affected Subsystem:** Module_05_Continuous_and_Dynamic_Batching
- **Reported Impact:** After migrating from static to continuous batching, GPU
  utilization graphs still show slots sitting idle while a queue of waiting
  requests builds up, and end-to-end completion time for a mixed workload
  barely improved.

---

## Observable Symptoms & Logs
```text
Batch capacity=4. Initial batch req_1..req_4 need 2/3/4/5 steps; req_5/req_6
(waiting, 2 steps each) should backfill freed slots as they open.
Expected (true continuous batching): req_1's slot frees at step 2 and is
immediately backfilled, so req_5/req_6 finish by ~step 4 and the whole run
completes in ~5 steps.
Actual finish steps: {'req_1': 2, 'req_2': 3, 'req_3': 4, 'req_4': 5, 'req_5': 7, 'req_6': 7}
Actual total steps to drain all 6 requests: 7
```
`req_1` frees its slot at step 2, but `req_5` and `req_6` don't finish until
step 7 -- as if they never got a chance to start until the entire original
batch had drained, not the moment a slot opened up.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Continuous_and_Dynamic_Batching/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_continuous_batcher.py
   ```
3. Observe that the total step count to drain all 6 requests matches what a
   purely static (batch-of-batches) scheduler would need, not what a
   continuous scheduler should achieve.

---

## Your Objective
1. Inspect `run_scheduler()` and find exactly when new requests are admitted
   from `waiting` into `running`.
2. Compare that condition against what should trigger admission in true
   continuous batching (a single freed slot, not an empty batch).
3. Formulate a hypothesis for why req_5/req_6 sit in the queue long after a
   slot opens up, then check `ANSWERS.md`.
