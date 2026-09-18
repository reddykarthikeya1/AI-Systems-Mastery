# Debug Lab Incident Report: Hybrid Search's Best Result Never Appears in the Fused Ranking

- **Severity:** P1 Retrieval Correctness
- **Affected Subsystem:** Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion
- **Reported Impact:** A document ranked #1 by both the keyword (BM25) and
  vector retrievers -- the clearest possible hybrid-search signal -- is
  completely missing from the final fused results shown to users, while
  weaker, lower-ranked documents appear at the top instead.

---

## Observable Symptoms & Logs
```text
BM25 ranked list:   ['doc_A', 'doc_B', 'doc_C', 'doc_D']
Vector ranked list: ['doc_A', 'doc_C', 'doc_E', 'doc_B']
doc_A is the #1 hit in BOTH retrievers -- the strongest possible signal a
hybrid search system can get.

Expected: doc_A should have the HIGHEST fused score and lead the final
ranking.
Actual fused scores: {'doc_B': 1.3333, 'doc_C': 1.5, 'doc_D': 0.3333, 'doc_E': 0.5}
Actual fused ranking (best to worst): ['doc_C', 'doc_B', 'doc_E', 'doc_D']
Is doc_A present in the fused scores at all? False
```
`doc_A` never shows up in `fused_scores` at all -- not with a low score, but
completely absent -- despite topping both input rankings.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_Hybrid_Search_and_Reciprocal_Rank_Fusion/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_rrf_fusion.py
   ```
3. Observe that `doc_A`, ranked first in both source lists, has no entry at
   all in the resulting `fused_scores` dictionary.

---

## Your Objective
1. Inspect `reciprocal_rank_fusion()` and trace exactly what happens on the
   very first iteration of the inner loop, when `rank == 0`.
2. Consider what `except ZeroDivisionError: continue` actually does to that
   iteration versus what should happen for the top-ranked document in a list.
3. Formulate a hypothesis for why a document's contribution -- and in this
   case, the document itself -- disappears when it ranks first, then check
   `ANSWERS.md`.
