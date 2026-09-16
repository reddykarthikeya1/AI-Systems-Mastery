# Phase 6 Checkpoint — Greedy and Exhaustive Search

- **Curriculum Modules:** Modules 12 - 13 (Greedy Algorithms and Interval Scheduling, Backtracking and Constraint Satisfaction)

- [Module 12 — Greedy Algorithms and Interval Scheduling](../Module_12_Greedy_Algorithms_and_Interval_Scheduling/01_README.md)
- [Module 13 — Backtracking and Constraint Satisfaction](../Module_13_Backtracking_and_Constraint_Satisfaction/01_README.md)

---

## What this checkpoint proves

You can tell a provable greedy from a plausible one, and you can enumerate
configurations without corrupting the results.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Prove, by an exchange argument, that sorting intervals by end time maximises the
number of non-overlapping selections — then produce an input where sorting by
start gives a strictly worse answer.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_12_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. State the interval rule for merging versus scheduling, and give an input distinguishing them.
2. Name the two most common backtracking bugs and the one-line fix for each.
3. Explain what `i > start and a[i] == a[i-1]` does, and why the `i > start` half is essential.
4. Say what you should do when you cannot prove a greedy choice is safe.

---

## Passing criteria

- [ ] Every problem in Modules 12–13 passes from `problems/`
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

- Question 1 → revisit the relevant module's README section and the `max_non_overlapping` problem
- Question 2 → revisit the relevant module's README section and the `subsets` problem
- Question 3 → revisit the relevant module's README section and the `combination_sum` problem
- Question 4 → revisit the relevant module's README section and the `combination_sum` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 5](PHASE_05_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 7 →](PHASE_07_CHECKPOINT.md)
