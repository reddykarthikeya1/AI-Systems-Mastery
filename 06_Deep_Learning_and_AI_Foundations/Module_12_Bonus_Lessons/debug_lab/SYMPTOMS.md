# Debug Lab Incident Report: Semantic Search Ranks an Unrelated Document Above a Closely Related One

- **Severity:** P2 Retrieval Quality
- **Affected Subsystem:** Module_12_Bonus_Lessons
- **Reported Impact:** A minimal semantic search demo ranks candidate embeddings against a query embedding to find the closest match. A candidate that points in almost the exact same direction as the query loses out to a candidate that points in a very different direction but happens to have a much larger vector magnitude.

---

## 🚨 Observable Symptoms & Logs
```text
Query embedding: [1.0, 0.0]
Ranked nearest neighbors (highest score first):
  unrelated_long_document: score=3.000
  closely_related_short: score=0.900
  opposite_direction: score=-1.000
Top match chosen: 'unrelated_long_document'
```
`closely_related_short` ([0.9, 0.1]) is nearly parallel to the query ([1.0, 0.0]), while `unrelated_long_document` ([3.0, 5.0]) points in a mostly orthogonal direction. A direction-based similarity search should clearly prefer the closely related candidate, but it is not the top match.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_12_Bonus_Lessons/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_embedding_similarity.py
   ```
3. Compare the printed ranking order to the geometric direction of each candidate vector relative to the query.

---

## 🎯 Your Objective
1. Inspect `broken_embedding_similarity.py`'s `similarity()` function.
2. Work out what quantity `dot(query, candidate)` actually measures, and how it is affected by each vector's magnitude versus its direction.
3. Formulate a hypothesis for why the long, unrelated vector wins, then check `ANSWERS.md`.
