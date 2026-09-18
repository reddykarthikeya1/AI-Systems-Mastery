# Debug Lab Incident Report: Evaluation Harness Rewards a Task That Failed Immediately With a Higher Efficiency Score Than One That Succeeded

- **Severity:** P2 Evaluation Validity
- **Affected Subsystem:** Module_08_Production_Agent_Evaluation
- **Reported Impact:** A model-selection dashboard driven by this harness's efficiency metric ranked a checkpoint that failed almost every task above one that reliably completed them, because tasks the agent gave up on quickly scored as "highly efficient."

---

## 🚨 Observable Symptoms & Logs
```text
Task A -- SUCCEEDED in 40 steps (optimal=10): efficiency score = 0.25
Task B -- FAILED after only 2 steps (optimal=10): efficiency score = 5.0
Failed task scores higher than the successful one: True
```
Both scores come straight out of `BrokenHarness.score()`, called with the same `optimal` step count for both tasks. Task A actually completed the objective, just less efficiently than the ideal plan. Task B never completed anything -- the agent gave up or crashed after only 2 steps. Despite that, Task B's efficiency score (`5.0`) is twenty times higher than Task A's (`0.25`), and a `success` flag was passed into `score()` for both calls.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_Production_Agent_Evaluation/debug_lab
   ```
2. `broken_harness.py` only defines `BrokenHarness`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_harness import BrokenHarness

   harness = BrokenHarness()

   # Task A: the agent SUCCEEDED, but took 40 steps against an optimal 10-step plan.
   success_score = harness.score(optimal=10, actual=40, success=True)

   # Task B: the agent FAILED (gave up / crashed) after just 2 steps.
   failure_score = harness.score(optimal=10, actual=2, success=False)

   print(f"Task A -- SUCCEEDED in 40 steps (optimal=10): efficiency score = {success_score}")
   print(f"Task B -- FAILED after only 2 steps (optimal=10): efficiency score = {failure_score}")
   print(f"Failed task scores higher than the successful one: {failure_score > success_score}")
   ```
3. Observe that the failed task's score is dramatically higher than the successful task's score, purely because it took fewer steps to give up.

---

## 🎯 Your Objective
1. Inspect `score()`'s parameters -- `success` is passed in, but where in the return statement is it actually read?
2. Compute `score(optimal=10, actual=2, success=False)` by hand and compare it to `score(optimal=10, actual=40, success=True)`.
3. Formulate a hypothesis for what the formula should do differently depending on whether `success` is `True` or `False`, then check `ANSWERS.md`.
