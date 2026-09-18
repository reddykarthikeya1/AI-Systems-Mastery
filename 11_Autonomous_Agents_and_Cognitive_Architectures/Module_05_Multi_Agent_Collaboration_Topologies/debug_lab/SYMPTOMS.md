# Debug Lab Incident Report: Multi-Agent Swarm Hands Off Forever in a Delegation Cycle and Never Reports "Done"

- **Severity:** P1 Runaway Cost / Availability
- **Affected Subsystem:** Module_05_Multi_Agent_Collaboration_Topologies
- **Reported Impact:** A three-agent planner/researcher/critic pipeline that was supposed to converge on a final draft instead kept handing the task back and forth between agents indefinitely, with each handoff triggering a new LLM call, until the run had to be killed manually after exhausting the team's API quota.

---

## 🚨 Observable Symptoms & Logs
```text
Delegation topology: planner -> researcher -> critic -> planner -> ...
HARNESS ABORT: harness force-stopped the run after 5001 handoffs -- BrokenSwarm.run() never reached 'Done'
Total handoffs before the forced abort: 5001
```
Each individual handoff looks correct in isolation -- `planner` hands to `researcher`, `researcher` hands to `critic`, and every `get_next()` call returns a perfectly valid next-agent name. The problem only becomes visible once the topology loops back on itself: `critic` hands control back to `planner`, and the run keeps going, handoff after handoff, without ever reaching the `"Done"` return. The 5,001 handoffs above are not a natural stopping point -- that is simply where an external safety cap intervened; nothing inside `BrokenSwarm.run()` itself brought the run to a halt.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Multi_Agent_Collaboration_Topologies/debug_lab
   ```
2. `broken_swarm.py` only defines `BrokenSwarm`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_swarm import BrokenSwarm

   calls = {"n": 0}
   SAFETY_CAP = 5000

   class Agent:
       def __init__(self, name, next_name):
           self.name = name
           self.next_name = next_name

       def get_next(self):
           calls["n"] += 1
           if calls["n"] > SAFETY_CAP:
               raise RuntimeError(
                   f"harness force-stopped the run after {calls['n']} handoffs -- "
                   "BrokenSwarm.run() never reached 'Done'"
               )
           return self.next_name

   swarm = BrokenSwarm({
       "planner": Agent("planner", "researcher"),
       "researcher": Agent("researcher", "critic"),
       "critic": Agent("critic", "planner"),  # hands back to planner
   })

   print("Delegation topology: planner -> researcher -> critic -> planner -> ...")
   try:
       swarm.run("planner", "draft a market analysis")
   except RuntimeError as e:
       print(f"HARNESS ABORT: {e}")
   print(f"Total handoffs before the forced abort: {calls['n']}")
   ```
3. Observe that the handoff count climbs into the thousands with no sign of stopping, and that only the harness's own `SAFETY_CAP` -- not anything inside `BrokenSwarm` -- is what eventually ends the run.

---

## 🎯 Your Objective
1. Inspect the `while True:` loop in `run()` and identify its only exit condition (`target` being falsy).
2. Trace the delegation chain configured in the reproduction: `planner -> researcher -> critic -> planner`. Does anything in `run()` detect that `curr` has returned to a previously visited agent?
3. Formulate a hypothesis for what should happen the second time control reaches an agent it has already visited, then check `ANSWERS.md`.
