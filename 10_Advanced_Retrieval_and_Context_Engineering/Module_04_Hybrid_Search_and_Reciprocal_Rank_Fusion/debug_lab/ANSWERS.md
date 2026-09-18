# Debug Lab Solution & Forensic Post-Mortem

## Incident: Hybrid Search's Best Result Never Appears in the Fused Ranking

---

### Forensic Root Cause Analysis
`reciprocal_rank_fusion()` enumerates each ranked list starting at `rank = 0`
and computes each document's contribution as `1 / rank`:

```python
for rank, doc_id in enumerate(ranked_list):
    try:
        contribution = 1 / rank
    except ZeroDivisionError:
        continue  # this document's rank-0 contribution is skipped
    scores[doc_id] = scores.get(doc_id, 0.0) + contribution
```

Standard Reciprocal Rank Fusion scores a document at rank `r` as
`1 / (k + r)` (using a 1-indexed rank, or an added constant `k`, specifically
so the #1 result never triggers a division by zero). Here `rank` starts at 0,
so the very first document in every list computes `1 / 0`, raises
`ZeroDivisionError`, and hits `continue` -- which skips `scores[doc_id] = ...`
for that iteration entirely. Because `doc_A` sits at rank 0 in *both* input
lists, it never receives a score contribution from either one, so it never
gets an entry in `scores` at all -- not a low score, no entry whatsoever. The
`try/except` doesn't fix the underlying off-by-one; it just converts a crash
into a silent, undetected data-loss bug.

---

### Production Corrective Action & Code Fix

```python
def reciprocal_rank_fusion(ranked_lists, k=60):
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list, start=1):
            contribution = 1 / (k + rank)
            scores[doc_id] = scores.get(doc_id, 0.0) + contribution
    return scores
```

Starting `rank` at 1 (or adding a constant `k`, as real RRF implementations
do) means `contribution` is always a well-defined positive number, no
`try/except` is needed, and `doc_A` -- ranked #1 in both lists -- now
receives the largest score and leads the fused ranking, exactly as expected.

---

### Production Prevention Invariants
1. **Never Let a Caught Exception Silently Drop Data:** A `try/except` that
   swallows an error and `continue`s past a write is a red flag; either fix
   the root cause so the exception can't occur, or make the skip loud
   (log, counter, alert) so silent data loss is detectable.
2. **Rank Convention Test:** RRF (and any rank-based scoring) implementation
   should have a unit test asserting the #1-ranked document in a single input
   list receives a nonzero, finite score -- this single case exposes an
   off-by-one in the rank origin immediately.
3. **Zero Documents Missing Invariant:** After fusion, assert that every
   distinct document id present in any input list also appears in the fused
   output; a document vanishing after fusion is never correct behavior.
