# Debug Lab Incident Report: In-Flight Request's KV Blocks Silently Reused

- **Severity:** P1 Cache Corruption
- **Affected Subsystem:** Module_02_KV_Cache_Memory_Management
- **Reported Impact:** Under sustained load with a full KV-cache block pool, a
  new request's allocation reused a block that an older, still-decoding
  request was actively reading from, corrupting that request's attention
  output mid-generation.

---

## Observable Symptoms & Logs
```text
req_a still in-flight, holds blocks: [0, 1, 2, 3]
req_b newly allocated blocks:       [0]
Expected: eviction should never hand out a block from req_a while refcount > 0
(req_a is still decoding).
Actual: block(s) reused from req_a's live set: [0]
req_a block refcounts after req_b's allocation: {0: 2, 1: 1, 2: 1, 3: 1}
```
Block `0` appears in both `req_a`'s live block list and `req_b`'s freshly
allocated blocks, and its refcount reads `2` even though only `req_b`'s
allocation should have touched it.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_KV_Cache_Memory_Management/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_kv_cache_evictor.py
   ```
3. Observe that a block belonging to the still-decoding `req_a` shows up in
   `req_b`'s newly allocated set.

---

## Your Objective
1. Inspect `KVCacheManager._evict_one()` and trace exactly which block it
   selects as the victim when the pool is exhausted.
2. Compare that against `refcount`, which tracks whether a block is still
   being read by an in-flight request.
3. Formulate a hypothesis for why the evictor is willing to hand out a block
   that is still referenced, then check `ANSWERS.md`.
