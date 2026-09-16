# Phase 5 Checkpoint — Dynamic Programming

- **Curriculum Modules:** Modules 10 - 11 (Dynamic Programming 1D and Sequence Patterns, Dynamic Programming 2D Knapsack and Grids)

- [Module 10 — Dynamic Programming 1D and Sequence Patterns](../Module_10_Dynamic_Programming_1D_and_Sequence_Patterns/01_README.md)
- [Module 11 — Dynamic Programming 2D Knapsack and Grids](../Module_11_Dynamic_Programming_2D_Knapsack_and_Grids/01_README.md)

---

## What this checkpoint proves

You can answer the four DP questions — state, transition, base case, order — on
an unseen problem, and you know which loop direction each knapsack variant needs.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Implement 0/1 knapsack with a single rolling row, then change one thing to make
it unbounded knapsack, and state precisely what that one thing was.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_10_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. List the four questions, in order, and say which one being wrong cannot be fixed by debugging the others.
2. Explain why the 0/1 knapsack rolling row iterates capacity downward, and what happens upward.
3. Give a problem where a single running maximum is insufficient state, and say what the second value is.
4. Explain why 'find all solutions' rules out DP.

---

## Passing criteria

- [ ] Every problem in Modules 10–11 passes from `problems/`
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

- Question 1 → revisit the relevant module's README section and the `knapsack_01` problem
- Question 2 → revisit the relevant module's README section and the `max_product_subarray` problem
- Question 3 → revisit the relevant module's README section and the `coin_change_min` problem
- Question 4 → revisit the relevant module's README section and the `coin_change_min` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 4](PHASE_04_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 6 →](PHASE_06_CHECKPOINT.md)
