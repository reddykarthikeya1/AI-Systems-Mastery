# Debug Lab Solution & Forensic Post-Mortem

## Incident: Nearest-Neighbor Search Returns the Most Distant Match

---

### Forensic Root Cause Analysis
`nearest_centroid_for_insert()` and `nearest_centroid_for_query()` are
supposed to do the exact same computation -- find the closest centroid to a
vector -- but they use opposite comparison functions:

```python
def nearest_centroid_for_insert(vector):
    return min(CENTROIDS, key=lambda name: l2_distance(vector, CENTROIDS[name]))

def nearest_centroid_for_query(vector):
    return max(CENTROIDS, key=lambda name: l2_distance(vector, CENTROIDS[name]))
```

`min(...)` correctly picks the centroid with the *smallest* distance, so
vectors get clustered into the geometrically correct bucket at insert time.
`max(...)` picks the centroid with the *largest* distance, so at query time
the index deliberately selects the partition the query is farthest from. An
IVF index's entire performance argument rests on "the true nearest neighbors
of a query are overwhelmingly likely to live in the query's own partition, so
we only need to scan that partition" -- inverting the centroid selection at
query time breaks that guarantee completely: the index scans the one
partition guaranteed *not* to contain nearby vectors (assuming a well
clustered dataset), so results in the correct partition are missed.

---

### Production Corrective Action & Code Fix

```python
def nearest_centroid_for_query(vector):
    return min(CENTROIDS, key=lambda name: l2_distance(vector, CENTROIDS[name]))
```

With both functions using `min()`, the query `(0.2, 0.3)` correctly resolves
to `bucket_a`, and `search()` scans `doc_1`, `doc_2`, and `doc_3`, returning a
top-1 result with distance well under 1.0 instead of the 13.7-distance
outlier from `bucket_b`.

---

### Production Prevention Invariants
1. **Share One Implementation, Not Two Copies:** Insert-time and query-time
   partition lookup must call the *same* nearest-centroid function; having
   two independently written copies is exactly how they silently drift apart
   (here, into literal opposites).
2. **Self-Consistency Test:** For any vector already in the index, assert
   that searching with that exact vector as the query returns the partition
   it was inserted into, and finds itself as (one of) the top results.
3. **Recall Sanity Check:** Compare a small sample of partitioned-search
   results against brute-force search over the same data; a recall collapse
   after enabling partitioning, as seen here, points squarely at the
   partition-selection logic, not the distance metric or the data itself.
