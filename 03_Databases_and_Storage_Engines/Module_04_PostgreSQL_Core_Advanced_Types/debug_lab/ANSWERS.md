# Debug Lab Solution & Forensic Post-Mortem

## Incident: Sequential Scan on 5,000,000 JSONB Document Catalog

---

### 🔍 Forensic Root Cause Analysis
`query_text_extract_eq()` models the `data->>'status' = 'active'` text-extraction
operator, which has no relationship to the GIN index built on `(key, value)`
containment pairs. Postgres's `gin_path_ops`/default GIN opclasses only
accelerate the `@>` containment operator (and a few others), not `->>` text
comparisons, so the planner has no index it can use and must evaluate the
predicate against every row.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def query_containment(self, key, value):
    """Equivalent to `data @> '{"key": "value"}'::jsonb` -- servable by the GIN index."""
    ids = self.gin_index.get((key, value), set())
    return sorted(ids), len(ids)
```

In SQL, rewrite the filter to use containment instead of extraction:
```sql
-- was: WHERE data->>'status' = 'active'
WHERE data @> '{"status": "active"}'::jsonb
```

---

### 🛡️ Production Prevention Invariants
1. **Match the operator to the index:** GIN/`jsonb_path_ops` indexes only serve
   `@>`, `?`, `?|`, `?&` -- audit any `->>`/`->` filter on an indexed JSONB column.
2. **`EXPLAIN ANALYZE` in CI** for hot JSONB queries, failing the build on a
   `Seq Scan` over tables above a row-count threshold.
3. **Expression indexes** as a fallback when the extraction operator is
   genuinely required (`CREATE INDEX ON t ((data->>'status'))`).
