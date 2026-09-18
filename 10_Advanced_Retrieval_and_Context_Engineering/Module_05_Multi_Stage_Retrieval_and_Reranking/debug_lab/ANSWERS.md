# Debug Lab Solution & Forensic Post-Mortem

## Incident: Reranker Promotes the Least Relevant Passage to #1

---

### Forensic Root Cause Analysis
`word_overlap_distance()` returns a *distance* (smaller = more relevant), and
`distance_to_similarity()` correctly inverts it into a *similarity* score
(larger = more relevant). But `rerank()`'s final sort still sorts ascending,
which was the right direction for the distance the pipeline started with,
not the similarity it ends with:

```python
scored.sort(key=lambda item: item[2])  # sort by the cross-encoder score
```

`sort()` defaults to ascending order. Once `item[2]` holds a similarity
score, ascending order puts the *lowest*-similarity (least relevant)
candidate first and the *highest*-similarity (most relevant) candidate last
-- exactly the reverse of what a reranker should do. The conversion from
distance to similarity happened correctly; the sort direction simply never
got updated to match the new "bigger is better" convention.

---

### Production Corrective Action & Code Fix

```python
scored.sort(key=lambda item: item[2], reverse=True)  # highest similarity first
```

With `reverse=True`, the list is sorted from highest similarity to lowest, so
`doc_1` and `doc_3` (both similarity 0.8000, directly about defective-item
returns) lead the reranked results, and `doc_2` (store hours, similarity
0.5000) correctly falls to the bottom.

---

### Production Prevention Invariants
1. **Sort Direction Must Match the Metric's Polarity:** Every sort on a score
   needs an explicit, commented decision about ascending vs. descending tied
   to what the score means (distance: ascending; similarity: descending) --
   never leave it to the default.
2. **Known-Relevant Fixture Test:** Rerankers should be tested against a
   fixture with an obviously relevant and an obviously irrelevant candidate,
   asserting the relevant one lands first after reranking.
3. **Sanity-Check After Every Score Transform:** Any time a score is
   transformed (distance -> similarity, logit -> probability, etc.),
   immediately verify the consumer of that score (sort, threshold comparison)
   was updated to match the new direction -- transforms and their consumers
   drift apart exactly like this.
