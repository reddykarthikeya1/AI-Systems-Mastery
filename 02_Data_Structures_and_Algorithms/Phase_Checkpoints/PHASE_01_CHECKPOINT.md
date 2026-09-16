# Phase 1 Checkpoint — Cost and Contiguous Memory

- **Curriculum Modules:** Modules 01 - 02 (Complexity Analysis and Memory Layout, Arrays Dynamic Arrays and Strings)

- [Module 01 — Complexity Analysis and Memory Layout](../Module_01_Complexity_Analysis_and_Memory_Layout/01_README.md)
- [Module 02 — Arrays Dynamic Arrays and Strings](../Module_02_Arrays_Dynamic_Arrays_and_Strings/01_README.md)

---

## What this checkpoint proves

You can predict an algorithm's cost before writing it, and you can turn a
quadratic scan over an array into a linear one.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Given an unseen array problem with `n <= 10**5`, decide in under 60 seconds
whether it wants two pointers, a sliding window, prefix sums, or binary search on
the answer — and justify the choice from the constraint alone.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_01_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. State the complexity budget for n = 10, 20, 5000, 10**5 and 10**9 without looking it up.
2. Explain why a sliding window is invalid for 'subarray sums to exactly k' when values may be negative, and what replaces it.
3. Given a problem whose answer ranges to 10**9 but whose input is only 10**4 items, name the technique and say why the mismatch is the signal.
4. Derive the total element copies for n appends under doubling, and show the per-append average is bounded.

---

## Passing criteria

- [ ] Every problem in Modules 01–02 passes from `problems/`
- [ ] Every module starter in this phase still **fails** before you start it
      (`make integrity`)
- [ ] You have worked the debug lab for each module in this phase and written a
      diagnosis for every symptom **before** opening `ANSWERS.md`
- [ ] You can answer all 4 diagnostic questions without reference
- [ ] You can state the complexity of every solution you wrote, and check it
      against the stated constraint

## If you cannot pass it

Do not repeat the whole phase. The diagnostic questions map to specific
material:

- Question 1 → revisit the relevant module's README section and the `max_window_sum` problem
- Question 2 → revisit the relevant module's README section and the `subarray_sum_k` problem
- Question 3 → revisit the relevant module's README section and the `min_ship_capacity` problem
- Question 4 → revisit the relevant module's README section and the `min_ship_capacity` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 2 →](PHASE_02_CHECKPOINT.md)
