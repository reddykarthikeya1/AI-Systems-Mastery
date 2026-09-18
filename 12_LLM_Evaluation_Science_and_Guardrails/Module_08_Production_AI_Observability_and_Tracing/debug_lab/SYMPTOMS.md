# Debug Lab Incident Report: Observability Tracer Drops Latency, Time-to-First-Token, and Cost From Every LLM Call Trace

- **Severity:** P2 Observability Gap
- **Affected Subsystem:** Module_08_Production_AI_Observability_and_Tracing
- **Reported Impact:** A cost-monitoring dashboard built on top of this tracer's output showed $0 spend and no latency data for every LLM call in production, even during an incident where response times had visibly degraded and the month's API bill had tripled. None of that signal ever reached the trace records.

---

## 🚨 Observable Symptoms & Logs
```text
Trace object emitted for this LLM call: {'tokens': 1523}
Does the trace capture latency/duration? False
Does the trace capture time-to-first-token? False
Does the trace capture monetary cost? False
```
`record()` returns a trace object without raising any error, and the object does contain a token count -- it looks like a working trace at first glance. Checking what fields are actually present shows the trace has nothing about how long the call took, nothing about time-to-first-token, and nothing about what the call cost, even though the call being traced represented a real request with all three of those properties.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_Production_AI_Observability_and_Tracing/debug_lab
   ```
2. `broken_tracer.py` only defines `BrokenTracer`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_tracer import BrokenTracer

   tracer = BrokenTracer()

   # The real API call this trace is describing took 2.4s end-to-end, 0.6s to
   # first token, and billed $0.018 -- record() isn't given the chance to
   # capture any of that.
   trace = tracer.record(model="gpt-4o", tokens=1523)

   print(f"Trace object emitted for this LLM call: {trace}")
   print(f"Does the trace capture latency/duration? {'latency' in trace or 'duration' in trace}")
   print(f"Does the trace capture time-to-first-token? {'ttft' in trace}")
   print(f"Does the trace capture monetary cost? {'cost' in trace}")
   ```
3. Observe that the emitted trace contains only `tokens`, and that latency, time-to-first-token, and cost are all absent regardless of what actually happened during the call being traced.

---

## 🎯 Your Objective
1. Inspect `record()`'s parameters -- what information about the call does it accept at all?
2. Compare that against what a production trace of an LLM call would need to answer "how slow was this?" and "how much did this cost?"
3. Formulate a hypothesis for what fields and inputs `record()` is missing, then check `ANSWERS.md`.
