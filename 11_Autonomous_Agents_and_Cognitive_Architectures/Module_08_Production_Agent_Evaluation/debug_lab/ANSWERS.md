# Debug Lab Solution & Forensic Post-Mortem

## Incident: Evaluation Harness Rewards a Task That Failed Immediately With a Higher Efficiency Score Than One That Succeeded

---

### 🔍 Forensic Root Cause Analysis
`score()` accepts a `success` flag as a parameter but never reads it in the return statement:

```python
def score(self, optimal, actual, success):
    return optimal / actual
```

The function always evaluates the same pure step-efficiency ratio, `optimal / actual`, which by construction rewards finishing in fewer steps -- regardless of whether the task was actually completed. A task that fails almost immediately produces a small `actual` step count and therefore an inflated ratio (`10 / 2 = 5.0`), while a task that succeeds but takes longer produces a larger `actual` and a lower ratio (`10 / 40 = 0.25`). The metric literally cannot distinguish "finished fast" from "gave up fast," because the one piece of information that would tell them apart, `success`, is accepted as an argument and then discarded.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedHarness:
    def score(self, optimal, actual, success):
        if not success:
            return 0.0
        return optimal / actual
```

Gating on `success` before computing the ratio means a failed task can never outscore a successful one -- it always scores `0.0` regardless of how few steps it took, and the step-efficiency ratio is only ever meaningful for tasks that actually completed.

---

### 🛡️ Production Prevention Invariants
1. **Gate on Success, Don't Blend It Into a Continuous Formula:** Any efficiency/quality metric that accepts a success flag must branch on it explicitly, not average it away inside an arithmetic expression.
2. **Regression-Test the Ordering Invariant:** Add a test asserting `failure_score <= success_score` for every matched pair of `optimal`/`actual` values, so an inverted metric fails CI instead of shipping to a dashboard.
3. **Report Success Rate and Efficiency-Given-Success Separately:** Never conflate the two into one number; a model-selection dashboard needs both signals independently to make a sound comparison.
