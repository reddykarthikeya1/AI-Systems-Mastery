# Module_20_Performance_Optimization_Profiling_Caching: Project Implementation Guide

**Deliverable:** an ultra-low-latency two-tier cache with LRU eviction, monotonic TTLs, thundering herd dogpiling protection, and Redis L2 persistence.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_cache_engine.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — O(1) LRU Cache Algorithm
Implement L1 memory cache using doubly-linked list or `collections.OrderedDict` achieving constant-time get, set, and eviction.

### Step 2 — Monotonic Clock Expiration
Compute item TTLs using `time.monotonic()` to prevent wall-clock NTP jumps from corrupting cache lifetime.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_cache_engine.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Cache Stampede / Thundering Herd Guard
Implement single-flight mutex locking ensuring 20 concurrent misses result in exactly 1 underlying database fetch.

### Step 4 — Two-Tier L1/L2 Coordination
Check L1 first; on miss, check L2 (Redis); on L2 hit, populate L1 before returning to caller.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/cache_engine.py`, replace `time.monotonic()` with `time.time()` in the expiration calculation.
Run:
```bash
pytest ../project_solution/test_cache_engine.py -k test_ttl_uses_monotonic_clock_not_wall_clock -v
```
Watch the test fail when simulated clock jump prematurely expires keys, then restore `time.monotonic()`.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_cache_engine.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Probabilistic Early Re-computation (XFetch):** Implement the XFetch algorithm to recompute hot keys before expiry.
2. **Adaptive Size-Aware Eviction:** Evict keys based on actual payload byte size rather than raw entry count.
3. **C-Accelerated Bloom Filter:** Add an in-memory Bloom filter to immediately reject non-existent keys.
4. **Cache Invalidation Pub/Sub:** Broadcast cache invalidation events across multiple L1 server instances.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_lru_operations_are_constant_time` | Proves get, set, and eviction operate in constant time O(1) |
| `test_ttl_uses_monotonic_clock_not_wall_clock` | Proves key TTLs are immune to system wall-clock adjustments |
| `test_cache_stampede_single_flight` | Proves concurrent requests for the same key trigger exactly 1 loader call |
| `test_cache_is_dramatically_faster_than_loader` | Proves cache hit is measurably faster than expensive origin loader |
| `test_cached_none_distinguishable_from_miss` | Proves negative caching (None value) does not trigger loader |

---

## 🎓 You have mastered this module when you can…

- [ ] Design constant-time O(1) LRU eviction algorithms using doubly-linked hash maps
- [ ] Explain why time.monotonic() must always be used for intervals rather than time.time()
- [ ] Prevent cache stampedes (dogpiling) using single-flight mutex locking
- [ ] Distinguish cached None values from genuine cache misses using sentinel objects
- [ ] Profile CPU bottlenecks using cProfile, py-spy, and flamegraphs
- [ ] Coordinate multi-tier caching architectures between in-memory L1 and network L2
- [ ] Write performance benchmark assertions asserting cache speedups in automated test suites
