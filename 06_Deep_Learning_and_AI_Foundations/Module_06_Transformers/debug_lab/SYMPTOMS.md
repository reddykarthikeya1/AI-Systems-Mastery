# Debug Lab Incident Report: Attention Weights Do Not Sum to One

- **Severity:** P2 Numerical Correctness
- **Affected Subsystem:** Module_06_Transformers
- **Reported Impact:** A hand-written self-attention layer is supposed to turn each
  token's raw similarity scores into a probability distribution over the other
  tokens (weights summing to 1.0 per query). The printed row sums don't match that
  invariant at all.

---

## Observable Symptoms & Logs
```text
Attention weight matrix (each row is one token's distribution over all keys):
  'the': [0.401, 0.292, 0.198]  row_sum=0.891
  'cat': [0.198, 0.292, 0.401]  row_sum=0.891
  'sat': [0.401, 0.416, 0.401]  row_sum=1.218
```
Every row is supposed to be a probability distribution (softmax output) and therefore
sum to `1.000`, but the rows sum to `0.891`, `0.891`, and `1.218`.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_Transformers/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_attention_normalization.py
   ```
3. Check each row's printed `row_sum` against the expected value of `1.0`.

---

## Your Objective
1. Inspect `broken_attention_normalization.py`'s `softmax_over_scores()` function.
2. Work out which axis of the `scores` matrix it normalizes over, versus which axis
   a per-query softmax is supposed to normalize over.
3. Formulate a hypothesis for the mismatched row sums, then check `ANSWERS.md`.
