# Debug Lab Solution & Forensic Post-Mortem

## Incident: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors

---

### 🔍 Forensic Root Cause Analysis
The index ranks candidates by raw dot product (`dot(query, candidate)`).
Unlike cosine similarity, the dot product is sensitive to each vector's
magnitude, not just its direction: `[3.0, -2.9]` scores higher than
`[0.9, 0.1]` against the query purely because its magnitude is larger, even
though its direction is far less aligned with the query. Because embeddings
were inserted with arbitrary, unnormalized magnitudes while the index metric
is dot product, vectors with large norms systematically dominate the ranking
regardless of actual semantic relevance.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def normalize(v):
    norm = math.sqrt(dot(v, v))
    return [x / norm for x in v]

# Insert-time fix: normalize every embedding before indexing --
# dot product on unit vectors IS cosine similarity.
normalized_candidates = {k: normalize(v) for k, v in candidates.items()}
```

Either normalize every embedding to unit length at insert time (so dot product
becomes equivalent to cosine similarity), or configure the index to use
cosine distance directly instead of raw dot product.

---

### 🛡️ Production Prevention Invariants
1. **Normalize embeddings at write time** whenever the index metric is dot
   product, and enforce it in the ingestion pipeline, not by convention.
2. **Match the distance metric to the embedding model's training objective**
   (many embedding models assume cosine similarity).
3. **Regression-test retrieval quality** with known relevant/irrelevant pairs
   of differing magnitude, not just differing direction.
