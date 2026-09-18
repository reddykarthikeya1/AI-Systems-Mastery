# Debug Lab Solution & Forensic Post-Mortem

## Incident: Deep Pagination Offset Crashes Elasticsearch Data Nodes

---

### 🔍 Forensic Root Cause Analysis
`deep_page_naive()` models `from`/`size` pagination: to return results 50,000
through 50,050, every shard must sort and return its own top `from + size`
(50,050) documents to the coordinating node, which then merges
`num_shards * (from + size)` documents in memory before trimming to the final
50. The deeper the offset, the more every shard -- and the coordinator -- must
sort and hold, independent of how many results are actually requested.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def search_after(self, size):
    """Each shard only ever needs to return `size` documents past a cursor,
    regardless of how deep into the result set that cursor is."""
    return size * self.num_shards
```

In Elasticsearch: replace `from`/`size` pagination past the first few pages
with `search_after` (cursor-based) or the Scroll/PIT API, neither of which
requires any shard to sort more than `size` documents per request.

---

### 🛡️ Production Prevention Invariants
1. **Cap `from + size`** (Elasticsearch's `index.max_result_window` default is
   10,000) and reject requests beyond it at the API layer.
2. **Use `search_after`/PIT for any UI that needs to page deep**, such as
   exports or infinite scroll.
3. **Monitor coordinator node heap usage** and alert on GC pressure correlated
   with pagination depth.
