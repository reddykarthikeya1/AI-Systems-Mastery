# Phase 4 Checkpoint — Graphs

- **Curriculum Modules:** Modules 08 - 09 (Graph Algorithms Traversals and DAGs, Graph Algorithms Shortest Paths and MST)

- [Module 08 — Graph Algorithms Traversals and DAGs](../Module_08_Graph_Algorithms_Traversals_and_DAGs/01_README.md)
- [Module 09 — Graph Algorithms Shortest Paths and MST](../Module_09_Graph_Algorithms_Shortest_Paths_and_MST/01_README.md)

---

## What this checkpoint proves

You can choose between BFS, DFS, Dijkstra and Bellman-Ford from the problem's
weights alone, and you know why directed cycle detection needs three states.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Given a weighted graph that may contain a negative edge, produce correct
shortest paths and detect whether the question is even well posed.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_08_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. State the decision rule linking edge weights to shortest-path algorithm, all four cases.
2. Draw a 4-node DAG that a two-state visited check wrongly reports as cyclic, and explain the third state.
3. Explain why marking BFS nodes on dequeue rather than enqueue degrades complexity.
4. Say what Bellman-Ford's n-th relaxation round is for, and what its result means.

---

## Passing criteria

- [ ] Every problem in Modules 08–09 passes from `problems/`
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

- Question 1 → revisit the relevant module's README section and the `has_cycle_directed` problem
- Question 2 → revisit the relevant module's README section and the `dijkstra` problem
- Question 3 → revisit the relevant module's README section and the `bellman_ford` problem
- Question 4 → revisit the relevant module's README section and the `bellman_ford` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 3](PHASE_03_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 5 →](PHASE_05_CHECKPOINT.md)
