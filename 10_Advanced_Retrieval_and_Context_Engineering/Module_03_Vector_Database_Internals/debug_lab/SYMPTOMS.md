# Debug Lab Incident Report: Nearest-Neighbor Search Returns the Most Distant Match

- **Severity:** P1 Retrieval Correctness
- **Affected Subsystem:** Module_03_Vector_Database_Internals
- **Reported Impact:** An IVF-partitioned vector index consistently returns
  results with huge distances from the query, even when nearly identical
  vectors are known to exist in the store. Recall dropped to near zero after
  partitioning was enabled, despite brute-force search over the same data
  working fine.

---

## Observable Symptoms & Logs
```text
Centroids: {'bucket_a': (0.0, 0.0), 'bucket_b': (10.0, 10.0)}
Stored vectors all cluster near (0, 0), so they were all inserted into:
['bucket_a', 'bucket_a', 'bucket_a']
Query vector (0.2, 0.3) is also near (0, 0).
Expected: search should scan 'bucket_a' (closest centroid to the query) and
return a very close match (distance well under 1.0).
Actual bucket searched: 'bucket_b'
Actual top-1 result: [('doc_4', 13.718600511714014)]
```
Three vectors sit within half a unit of the query, all in `bucket_a`, but
search reports scanning `bucket_b` and returns a result over 13 units away --
the single unrelated outlier vector that happens to live there.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_Vector_Database_Internals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_ivf_index.py
   ```
3. Observe that `search()` reports scanning `bucket_b` for a query vector
   that is obviously closest to `bucket_a`'s centroid, and returns a distant,
   low-quality match as a result.

---

## Your Objective
1. Inspect `nearest_centroid_for_insert()` and `nearest_centroid_for_query()`
   side by side and compare exactly how each one selects a centroid name
   from `CENTROIDS`.
2. Consider why insertion routes vectors correctly but query-time lookup
   picks a different bucket for a query sitting in the same region of space.
3. Formulate a hypothesis for why the two functions disagree, then check
   `ANSWERS.md`.
