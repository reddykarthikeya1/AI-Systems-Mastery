# Debug Lab Solution & Forensic Post-Mortem

## Incident: ZeRO Sharding Leaves a Tail of Parameters Permanently Stale

---

### 🔍 Forensic Root Cause Analysis
`partition_ranges()` computes `shard_size = num_params // world_size` using integer floor division and then gives every rank exactly `shard_size` parameters, covering a total of `world_size * shard_size` indices. When `num_params` is not evenly divisible by `world_size` (10 params / 4 ranks = 2 remainder 2), `world_size * shard_size` (4 * 2 = 8) is strictly less than `num_params` (10); the trailing `num_params % world_size` indices (here, indices 8 and 9) fall past every rank's `[lo, hi)` range and are never assigned to any rank at all. Because ZeRO gives each rank exclusive ownership of updating its shard, an index that belongs to no shard is never touched by any optimizer step -- there is no error, no exception, and no rank double-covers it either, so the model simply trains with two parameters silently frozen at their initial values, which is very difficult to detect from loss curves alone.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def partition_ranges(num_params, world_size):
    base_size = num_params // world_size
    remainder = num_params % world_size
    ranges = []
    start = 0
    for r in range(world_size):
        size = base_size + (1 if r < remainder else 0)  # give the first `remainder` ranks one extra
        ranges.append((start, start + size))
        start += size
    return ranges
```

---

### 🛡️ Production Prevention Invariants
1. **Always Handle the Remainder Explicitly:** Any even-partitioning scheme over `N` items across `W` workers must account for `N % W`, either by distributing the remainder across the first few shards (as above) or by giving the last shard the remainder; floor division alone silently drops items.
2. **Assert Full Coverage:** After computing shard ranges, assert that the union of all `[lo, hi)` ranges equals `range(num_params)` exactly -- no gaps, no overlaps -- as a startup-time sanity check before training begins.
3. **Test With Non-Divisible Sizes:** Always include a partitioning test where `num_params % world_size != 0`; a test suite that only uses evenly-divisible parameter counts can never expose a missing-remainder bug.
