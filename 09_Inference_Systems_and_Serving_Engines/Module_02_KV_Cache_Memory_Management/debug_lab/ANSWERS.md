# Debug Lab Solution & Forensic Post-Mortem

## Incident: In-Flight Request's KV Blocks Silently Reused

---

### Forensic Root Cause Analysis
`_evict_one()` pops the head of `lru_order` and returns it to the free pool
unconditionally:

```python
def _evict_one(self):
    victim = self.lru_order.pop(0)
    self.free_blocks.append(victim)
```

It never checks `self.refcount[victim]`. "Least recently used" is a fine tie
breaker among *unreferenced* blocks, but it says nothing about whether a block
is still owned by a live request. In the reproduction, `req_a`'s four blocks
are the entire LRU chain and `req_a` is still decoding (`refcount == 1` for
all four), yet `_evict_one()` happily reclaims block `0` -- the oldest entry
in that chain -- the moment `req_b` needs space. `req_b` then increments the
same block's refcount to `2` and starts writing its own KV entries into memory
`req_a` is still reading from mid-generation, corrupting `req_a`'s attention
output without ever raising an error.

---

### Production Corrective Action & Code Fix

```python
def _evict_one(self):
    for idx, candidate in enumerate(self.lru_order):
        if self.refcount[candidate] == 0:
            return self.lru_order.pop(idx) and self.free_blocks.append(candidate)
    raise MemoryError("no evictable (unreferenced) KV block available")
```

More precisely, the LRU chain should only ever contain blocks whose refcount
is zero (i.e. blocks get removed from `lru_order` the moment a request starts
using them and are only re-added to it -- and thus become eviction candidates
-- once every holder has released them). Eviction must be a *no-op or a hard
allocation failure*, never a silent steal, when every block in the pool is
still referenced.

---

### Production Prevention Invariants
1. **Refcount Before Reclaim:** Any cache evictor sharing memory across
   concurrent owners must check "is anyone still using this?" before
   "how old is this?" -- recency is only a valid eviction signal among
   otherwise-free resources.
2. **Invariant Assertion:** Assert `refcount[block] == 0` immediately before
   a block re-enters the free pool; trip a loud failure instead of a silent
   memory-safety violation.
3. **Backpressure Over Corruption:** When no evictable block exists, the
   correct behavior is to queue or reject the new allocation, not to borrow
   memory from a request that is still running.
