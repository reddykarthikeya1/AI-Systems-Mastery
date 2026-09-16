# Phase 7 Checkpoint — Advanced and Systems Structures

- **Curriculum Modules:** Modules 14 - 15 (Advanced Structures Trie UnionFind SegmentTree, Systems Level Structures SkipLists BloomFilters LRU)

- [Module 14 — Advanced Structures Trie UnionFind SegmentTree](../Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree/01_README.md)
- [Module 15 — Systems Level Structures SkipLists BloomFilters LRU](../Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU/01_README.md)

---

## What this checkpoint proves

You can pick the structure that matches the workload, and you understand which
guarantee each probabilistic structure trades away.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Given a workload of many range-sum queries interleaved with point updates,
choose between prefix sums, a Fenwick tree and a segment tree, and defend the
choice with complexities for both operations.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_14_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. State what a trie answers that a hash map cannot, and what union-find cannot do at all.
2. Explain the Bloom filter's one-sided guarantee, and which direction of error it permits.
3. Say why the k largest requires a min-heap while the k closest requires a max-heap.
4. Describe why an LRU cache needs both a hash map and a doubly linked list.

---

## Passing criteria

- [ ] Every problem in Modules 14–15 passes from `problems/`
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

- Question 1 → revisit the relevant module's README section and the `trie_operations` problem
- Question 2 → revisit the relevant module's README section and the `union_find` problem
- Question 3 → revisit the relevant module's README section and the `segment_tree` problem
- Question 4 → revisit the relevant module's README section and the `bloom_filter` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 6](PHASE_06_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md)
