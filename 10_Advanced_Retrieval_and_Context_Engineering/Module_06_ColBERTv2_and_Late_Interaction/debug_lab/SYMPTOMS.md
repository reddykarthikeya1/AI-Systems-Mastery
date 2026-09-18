# Debug Lab Incident Report: Late-Interaction Scoring Prefers Mediocre-Everywhere Docs Over Exact Matches

- **Severity:** P1 Retrieval Quality Regression
- **Affected Subsystem:** Module_06_ColBERTv2_and_Late_Interaction
- **Reported Impact:** A ColBERT-style late-interaction reranker consistently
  ranks documents that are vaguely on-topic throughout above documents that
  contain one precise, exact match for a key query term -- the opposite of
  what late interaction is supposed to reward.

---

## Observable Symptoms & Logs
```text
Query tokens: [(1.0, 0.0), (0.0, 1.0)]
doc_A tokens (one near-perfect match, one irrelevant): [(0.05, 0.99), (-1.0, 0.02)]
doc_B tokens (uniformly mediocre matches): [(0.5, 0.5), (0.45, 0.45)]

Expected: MaxSim should reward doc_A's exact per-term match, so score_a > score_b.
Actual score_a: 0.0347
Actual score_b: 1.4142
Actual winner: doc_B
```
`doc_A` contains a token that is a near-perfect match (cosine similarity
~0.99) for one of the two query tokens, yet it scores roughly 40x lower than
`doc_B`, whose tokens never closely match anything.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_ColBERTv2_and_Late_Interaction/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_colbert_maxsim.py
   ```
3. Observe that `score_a` is far lower than `score_b` despite `doc_A`
   containing an almost exact match for one query token.

---

## Your Objective
1. Inspect `late_interaction_score()` and trace exactly how `sims` (the list
   of per-document-token cosine similarities for one query token) gets
   reduced into a single number.
2. Compare that reduction against what "MaxSim" means by name -- what
   operation should turn a list of per-token similarities into the
   contribution for that query token?
3. Formulate a hypothesis for why doc_A's one excellent match gets buried,
   then check `ANSWERS.md`.
