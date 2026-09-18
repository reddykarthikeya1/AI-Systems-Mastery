# Debug Lab Solution & Forensic Post-Mortem

## Incident: ReAct Agent Loop Never Terminates When the LLM Stalls on Repeated Thoughts

---

### 🔍 Forensic Root Cause Analysis
`run()`'s `while True:` loop has exactly one exit path: finding the substring `"Final Answer:"` in the LLM's response. There is no iteration ceiling (`max_steps`), and there is no tracking of previously seen responses to detect that the LLM is stuck repeating itself. If the LLM never happens to emit that exact phrase -- because it is stuck reasoning in circles, degraded, or simply never reaches a conclusion for this goal -- the loop body has no other way to end. Each iteration calls `llm_fn(goal)` again, which in production means another full LLM request billed and latency added, forever. The 5,001 calls observed above is not a special number; it is simply wherever the external safety cap happened to be set, since nothing inside `BrokenReActEngine` would have stopped it at any point.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedReActEngine:
    def __init__(self, tools, max_steps=15):
        self.tools = tools
        self.max_steps = max_steps

    def run(self, goal, llm_fn):
        seen_responses = set()
        for step in range(self.max_steps):
            response = llm_fn(goal)
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()

            fingerprint = hash(response)
            if fingerprint in seen_responses:
                raise RuntimeError(
                    f"Cycle detected: identical response repeated after {step + 1} steps"
                )
            seen_responses.add(fingerprint)

        raise RuntimeError(f"Exceeded max_steps={self.max_steps} without a Final Answer")
```

Adding a hard `max_steps` ceiling guarantees the loop always terminates, win or lose. Fingerprinting each response and comparing it against everything seen so far in the same run additionally catches the common failure mode of the LLM repeating an identical thought, so the agent fails fast with a diagnosable error instead of silently spinning.

---

### 🛡️ Production Prevention Invariants
1. **Hard Step Ceiling:** Every agent loop must have a `max_steps`-style ceiling enforced in the loop itself, not bolted on by an external caller. An engine that can only be stopped by a wrapper around it is not safe to hand to a new caller who forgets to add one.
2. **Response Fingerprinting for Cycle Detection:** Track a hash/fingerprint of each step's output within a run and treat a repeat as a signal to abort, not just a step counter -- it catches stalls faster than waiting for the ceiling.
3. **Per-Run Call Count Telemetry:** Emit a metric for LLM calls per agent run and alert on runs that exceed a small multiple of the typical count, so a stuck agent is caught in minutes rather than discovered on the monthly bill.
