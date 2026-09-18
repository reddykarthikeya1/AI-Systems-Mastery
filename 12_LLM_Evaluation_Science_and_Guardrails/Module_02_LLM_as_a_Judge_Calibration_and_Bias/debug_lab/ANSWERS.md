# Debug Lab Solution & Forensic Post-Mortem

## Incident: LLM-as-Judge Comparison Always Favors Whichever Response Is Placed First

---

### 🔍 Forensic Root Cause Analysis
`evaluate()` calls `judge_fn` exactly once, in a single fixed order, and returns whatever it says:

```python
def evaluate(self, c1, c2, judge_fn):
    return judge_fn(c1, c2)
```

There is no second pass with `c1` and `c2` swapped, and no reconciliation between the two possible orderings. Position bias -- a well-documented tendency of LLM judges to favor whichever candidate occupies the first slot of the prompt -- is therefore never detected, let alone corrected. The reported "winner" tracks seat position at least as much as it tracks response quality: a judge function that is purely position-biased will produce the identical verdict ("A wins") no matter which response is actually better, because the two orderings are never compared against each other.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedJudge:
    def evaluate(self, c1, c2, judge_fn):
        first_pass = judge_fn(c1, c2)
        second_pass = judge_fn(c2, c1)      # swapped order

        winner_first = c1 if first_pass == "A" else c2
        winner_second = c2 if second_pass == "A" else c1

        if winner_first != winner_second:
            return "tie (position bias detected)"
        return winner_first
```

Running the comparison in both orderings and reconciling the results means a purely position-biased judge now produces a detected tie instead of a false, confident winner, and a genuinely discriminating judge still agrees with itself across both orderings.

---

### 🛡️ Production Prevention Invariants
1. **Run Every Pairwise Comparison in Both Orderings:** Disagreement between the two passes is a signal to surface, not noise to average away.
2. **Track Each Judge's "Prefers-Slot-A" Rate on a Calibration Set:** A rate far from 50% on known-tied pairs is a direct measurement of position bias that should gate whether the judge is trusted.
3. **Randomize Slot Assignment as a Complement, Not a Substitute:** Randomizing which candidate lands in which slot helps when averaging over many samples, but it does not replace explicitly checking both orderings for any single comparison that matters on its own.
