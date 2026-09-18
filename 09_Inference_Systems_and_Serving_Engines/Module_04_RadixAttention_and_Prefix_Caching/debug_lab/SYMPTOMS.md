# Debug Lab Incident Report: Shared System Prompt Never Hits the Prefix Cache

- **Severity:** P2 Cost/Latency Regression
- **Affected Subsystem:** Module_04_RadixAttention_and_Prefix_Caching
- **Reported Impact:** A fleet serving many requests that all share the same
  long system prompt shows zero prefix-cache hits and full KV recomputation
  on every request, despite RadixAttention being enabled specifically to
  reuse shared prefixes.

---

## Observable Symptoms & Logs
```text
All three requests share the same 6-token system prompt prefix:
  You are a helpful assistant .
Expected: request_b and request_c should HIT the cache entry request_a
populated for the shared system prompt (only 1 total KV compute).
  request_a: cache_hit=False
  request_b: cache_hit=False
  request_c: cache_hit=False
Actual total KV compute calls (should be 1 if the shared prefix were reused): 3
```
Three requests that all start with the exact same system-prompt tokens each
report `cache_hit=False`, and the cache performs a full compute for every one
of them instead of reusing the first request's work.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_RadixAttention_and_Prefix_Caching/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_radix_prefix_cache.py
   ```
3. Observe that `compute_calls` equals the number of requests instead of
   staying at 1 for the shared prefix.

---

## Your Objective
1. Inspect `RadixPrefixCache._cache_key()` and determine exactly which tokens
   of each request it uses to build the cache key.
2. Compare that against which tokens the three requests actually have in
   common.
3. Formulate a hypothesis for why requests that share a prefix never collide
   on the same cache key, then check `ANSWERS.md`.
