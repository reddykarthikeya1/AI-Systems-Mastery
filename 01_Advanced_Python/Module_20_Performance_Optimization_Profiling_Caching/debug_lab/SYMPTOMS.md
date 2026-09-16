# Debug Lab: Module 20 — Caching Traps

## How to Run
```bash
python debug_lab/broken_cache_engine.py
```

## Observed Symptoms
1. **Premature expiration or eternal caching under NTP skew**:
   Using `time.time()` causes entries to suddenly expire or live for hours if system time synchronizes backward.
2. **Cache Stampede on negative caching (Cached None treated as miss)**:
   `cache.get("user_404")` returns `None`, causing callers to treat it as a miss and hammer the origin database.
