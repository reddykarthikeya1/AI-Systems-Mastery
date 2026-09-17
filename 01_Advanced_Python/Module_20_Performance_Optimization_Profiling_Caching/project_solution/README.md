# Design Rationale: Two-Tier Resilient Cache & APM Telemetry Engine

## Architectural Overview
A high-performance caching subsystem integrating sub-microsecond in-process L1 caching (`lru_cache`), distributed Redis L2 caching, and single-flight cache stampede protection.

## Key Design Decisions
1. **Single-Flight Stampede Guard:** When a hot cached key expires, concurrent worker threads share a single in-flight loader promise, ensuring exactly 1 database query executes during miss storms.
2. **Two-Tier Cache Hierarchy (L1 RAM + L2 Redis):** Frequently accessed data is served from local process memory (< 100 ns), amortizing Redis network hops (1–2 ms) across high-traffic fleets.
3. **Probabilistic Early Expiration (XFetch):** Background workers refresh expiring keys before hard TTL expiration, preventing sudden latency spikes.

## Rejected Alternatives
1. **Unprotected Cache-Aside Pattern:**
   - *Reason for Rejection:* Under high concurrency (5,000 req/s), a cache expiration causes a thundering herd where all 5,000 requests query the database simultaneously, causing total database outage.
2. **Unbounded In-Memory Dictionaries:**
   - *Reason for Rejection:* Plain dictionaries without eviction limits leak memory indefinitely, leading to process termination by OS out-of-memory killers.

## Invariants & Guarantees
- 20 concurrent misses result in exactly 1 underlying database invocation.
- In-memory cache footprint is strictly bounded by maxsize eviction.

## Verification
```bash
pytest test_cache_engine.py -v
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

