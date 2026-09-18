# Debug Lab Incident Report: ReAct Agent Loop Never Terminates When the LLM Stalls on Repeated Thoughts

- **Severity:** P1 Runaway Cost / Availability
- **Affected Subsystem:** Module_01_Agent_Cognitive_Architectures_and_Loops
- **Reported Impact:** An agent deployment burned through its entire monthly LLM budget in under an hour after a routine goal caused the agent to loop indefinitely without ever producing a final answer. The client-facing request that triggered it never returned either, and the worker process had to be killed manually.

---

## 🚨 Observable Symptoms & Logs
```text
HARNESS ABORT: harness force-stopped the run after 5001 LLM calls -- BrokenReActEngine.run() never returned on its own
Total llm_fn calls before the forced abort: 5001
The goal string never changed and 'Final Answer:' was never produced.
```
Nothing about the goal or the tools looks wrong on inspection -- `BrokenReActEngine.run()` accepts a goal and an `llm_fn` exactly as documented, and it does return correctly whenever the LLM's response happens to contain `"Final Answer:"`. The problem only shows up when the LLM keeps "thinking" without ever emitting that phrase: the call count above did not stop climbing on its own, and the run above was only stopped because an external safety cap in the harness intervened at 5,000 calls and raised. Without that external cap, nothing inside `run()` itself would have stopped it.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_Agent_Cognitive_Architectures_and_Loops/debug_lab
   ```
2. `broken_react.py` only defines `BrokenReActEngine`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_react import BrokenReActEngine

   calls = {"n": 0}
   SAFETY_CAP = 5000

   def llm_fn(goal):
       calls["n"] += 1
       if calls["n"] > SAFETY_CAP:
           raise RuntimeError(
               f"harness force-stopped the run after {calls['n']} LLM calls -- "
               "BrokenReActEngine.run() never returned on its own"
           )
       return "Thought: I should look that up again before answering."

   engine = BrokenReActEngine(tools={})
   try:
       engine.run("What is the capital of France?", llm_fn)
   except RuntimeError as e:
       print(f"HARNESS ABORT: {e}")
   print(f"Total llm_fn calls before the forced abort: {calls['n']}")
   print("The goal string never changed and 'Final Answer:' was never produced.")
   ```
3. Observe that the call counter climbs into the thousands with no sign of slowing, and that only the harness's own `SAFETY_CAP` check -- not anything inside `BrokenReActEngine` -- is what eventually stops the run.

---

## 🎯 Your Objective
1. Inspect the `while True:` loop in `BrokenReActEngine.run()` and identify its only exit condition.
2. Trace what happens on every iteration when `llm_fn`'s response never contains `"Final Answer:"`.
3. Formulate a hypothesis for why the call count climbs without bound, then check `ANSWERS.md`.
