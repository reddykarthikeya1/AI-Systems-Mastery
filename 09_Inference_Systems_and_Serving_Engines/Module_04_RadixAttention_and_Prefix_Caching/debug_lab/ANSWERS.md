# Debug Lab Solution & Forensic Post-Mortem

## Incident: Shared System Prompt Never Hits the Prefix Cache

---

### Forensic Root Cause Analysis
`_cache_key()` builds its key from the *last* `CACHE_KEY_LEN` tokens of the
request instead of the first ones:

```python
def _cache_key(self, tokens):
    return tuple(tokens[-CACHE_KEY_LEN:])
```

`request_a`, `request_b`, and `request_c` all share the same leading 6-token
system prompt (`"You are a helpful assistant ."`) but have completely
different *trailing* tokens (`"is 2+2?"` vs. `"this doc."` vs. `"hello."`).
Keying on the suffix means the cache is effectively grouping requests by how
their *unique* user turn ends, which is almost never shared, instead of by
their *common* prefix, which is exactly what RadixAttention's radix tree is
built to detect and reuse. The result is a cache key space where collisions
between genuinely-shared prefixes are essentially impossible, so every
request takes the "compute from scratch" path.

---

### Production Corrective Action & Code Fix

```python
def _cache_key(self, tokens):
    # Key on the leading tokens -- the shared prefix -- not the trailing,
    # request-specific tokens, so requests with a common prefix collide on
    # the same cache entry the way a radix tree groups shared paths.
    return tuple(tokens[:CACHE_KEY_LEN])
```

(A real RadixAttention implementation walks a radix tree token-by-token to
find the longest matching prefix rather than truncating to a fixed length,
but the fix here restores the essential property this lab tests: the key must
be derived from the *shared* leading tokens, not the divergent trailing
ones.) With the fix, `request_a` computes the KV blocks once and
`request_b`/`request_c` both hit that entry, dropping `compute_calls` to 1.

---

### Production Prevention Invariants
1. **Key on What's Shared, Not What's Unique:** A cache's key must be derived
   from the dimension requests are expected to collide on; keying on a
   request-unique suffix guarantees near-zero hit rate no matter how good the
   cache data structure is.
2. **Hit-Rate Regression Test:** Any prefix-cache change should be covered by
   a test that sends N requests sharing a known prefix and asserts
   `compute_calls == 1` (or close to it), not just that no exception is
   raised.
3. **Instrument Cache Hit Rate in Production:** A near-zero hit rate on
   workloads with an obviously shared system prompt is a strong, cheap signal
   to alert on before it shows up as an infra cost or latency incident.
