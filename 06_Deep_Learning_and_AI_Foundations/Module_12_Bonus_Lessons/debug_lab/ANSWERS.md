# Debug Lab Solution & Forensic Post-Mortem

## Incident: Semantic Search Ranks an Unrelated Document Above a Closely Related One

---

### 🔍 Forensic Root Cause Analysis
`similarity()` returns the raw dot product `dot(query, candidate)` and calls it done, but a raw dot product is *not* a measure of directional similarity on its own -- it is directly proportional to each vector's magnitude as well as the angle between them. `unrelated_long_document` has a much larger norm than `closely_related_short`, so even though its direction is far less aligned with the query, its large magnitude inflates the dot product past that of the closely related candidate. True cosine similarity divides the dot product by the norms of *both* vectors specifically to cancel out this magnitude effect and leave only the directional (angular) component.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def norm(a):
    return math.sqrt(sum(x * x for x in a))

def similarity(query, candidate):
    denom = norm(query) * norm(candidate)
    return dot(query, candidate) / denom if denom > 0 else 0.0
```

Dividing by both vector norms turns the raw dot product into true cosine similarity. Once magnitude is cancelled out, `closely_related_short` scores far higher than `unrelated_long_document`, and the ranking correctly reflects directional closeness.

---

### 🛡️ Production Prevention Invariants
1. **Always Normalize for Similarity Search:** Use cosine similarity (or pre-normalize all embeddings to unit length) for any nearest-neighbor search, never a raw dot product, unless magnitude is deliberately meaningful.
2. **Magnitude Sanity Checks:** Log the norm distribution of a candidate set; wildly varying norms are a signal that a raw dot product will misbehave.
3. **Unit Tests With Known Geometry:** Keep a small fixture of vectors with known angles as a regression test for any similarity function.
