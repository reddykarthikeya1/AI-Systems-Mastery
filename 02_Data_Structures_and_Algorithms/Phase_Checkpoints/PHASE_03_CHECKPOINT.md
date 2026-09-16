# Phase 3 Checkpoint — Hierarchies and Priority

- **Curriculum Modules:** Modules 06 - 07 (Trees Binary Search Trees and Self Balancing, Heaps Priority Queues and TopK Patterns)

- [Module 06 — Trees Binary Search Trees and Self Balancing](../Module_06_Trees_Binary_Search_Trees_and_Self_Balancing/01_README.md)
- [Module 07 — Heaps Priority Queues and TopK Patterns](../Module_07_Heaps_Priority_Queues_and_TopK_Patterns/01_README.md)

---

## What this checkpoint proves

You can validate a tree invariant globally rather than locally, and you know
which heap to reach for when the problem says 'k-th'.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Write, without reference, a function returning the k-th smallest value in a BST
in O(height + k) — and say what makes it stop early rather than traversing the
whole tree.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_06_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. Show a 4-node tree that passes a parent/child BST check and is not a BST.
2. Explain why the k largest elements are kept in a MIN-heap, not a max-heap.
3. Describe the two-heap median invariant and what breaks if the rebalance is omitted.
4. State the difference between checking balance at the root and checking it at every node, in complexity terms.

---

## Passing criteria

- [ ] Every problem in Modules 06–07 passes from `problems/`
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

- Question 1 → revisit the relevant module's README section and the `is_valid_bst` problem
- Question 2 → revisit the relevant module's README section and the `kth_largest` problem
- Question 3 → revisit the relevant module's README section and the `streaming_median` problem
- Question 4 → revisit the relevant module's README section and the `streaming_median` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 2](PHASE_02_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 4 →](PHASE_04_CHECKPOINT.md)
