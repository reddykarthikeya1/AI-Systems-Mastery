# Debug Lab Incident Report: Reranker Promotes the Least Relevant Passage to #1

- **Severity:** P1 Retrieval Correctness
- **Affected Subsystem:** Module_05_Multi_Stage_Retrieval_and_Reranking
- **Reported Impact:** After adding a cross-encoder reranking stage on top of
  first-pass retrieval, answer quality got WORSE, not better -- the reranker
  now routinely promotes an off-topic passage above passages that directly
  answer the user's question.

---

## Observable Symptoms & Logs
```text
Query: 'return policy for defective items'
Candidates with their cross-encoder similarity scores (higher = more relevant):
  doc_2: sim=0.5000  'Our store hours are 9am to 9pm on weekdays.'
  doc_4: sim=0.6667  'We offer gift wrapping for an additional two dollars.'
  doc_1: sim=0.8000  'Defective items can be returned for a full refund within 30 days.'
  doc_3: sim=0.8000  'Broken or defective products qualify for free return shipping.'

Expected: the reranked list should lead with the MOST relevant passage
(highest similarity) about defective-item returns.
Actual #1 result after reranking: doc_2 -> 'Our store hours are 9am to 9pm on weekdays.'
```
`doc_2`, about store hours, has the LOWEST similarity score (0.5000) of the
four candidates, yet it's the first result returned. The two passages that
actually answer the query (`doc_1`, `doc_3`, both scoring 0.8000) end up last.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Multi_Stage_Retrieval_and_Reranking/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_reranker.py
   ```
3. Observe that the printed list is ordered from lowest similarity score to
   highest, and that the "actual #1 result" is the worst-scoring candidate.

---

## Your Objective
1. Inspect `rerank()` and check the `sort()` call's direction against what
   `distance_to_similarity()` says a "good" score looks like.
2. Trace `word_overlap_distance()` -> `distance_to_similarity()` end to end
   for `doc_1` and `doc_2` to confirm which one the cross-encoder actually
   considers more relevant.
3. Formulate a hypothesis for why the reranked list is backwards, then check
   `ANSWERS.md`.
