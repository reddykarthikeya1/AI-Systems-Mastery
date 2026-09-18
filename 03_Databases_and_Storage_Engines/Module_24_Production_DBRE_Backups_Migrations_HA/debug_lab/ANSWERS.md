# Debug Lab Solution & Forensic Post-Mortem

## Incident: Exclusive Table Lock Starvation During Online Schema Migration

---

### 🔍 Forensic Root Cause Analysis
`run_migration_no_timeout()` waits for the full duration of whatever already
holds the table (`slow_query_duration_ticks`) with no upper bound on how long
it is willing to wait. Because the migration is queued for an exclusive lock
ahead of ordinary application traffic, every incoming request submitted while
the migration waits queues up behind it too -- the migration never backs off,
so the queue grows for the entire 180-tick wait instead of the process
timing out and retrying with a brief, bounded lock acquisition window.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def run_migration_with_timeout(queue, incoming_requests, lock_timeout_ticks=5, retries=40):
    """Attempts the lock in short, bounded windows, backing off between
    attempts instead of parking indefinitely at the front of the lock queue."""
    for attempt in range(retries):
        acquired = try_acquire_lock(timeout_ticks=lock_timeout_ticks)
        if acquired:
            return attempt * lock_timeout_ticks
        # back off briefly; ordinary traffic is never blocked behind this wait
    raise TimeoutError("migration could not acquire the lock, will retry later")
```

In production: `SET lock_timeout = '2s';` before the `ALTER TABLE`, wrapped in
an application-level retry loop, or use an online schema-change tool
(`pt-online-schema-change`, `gh-ost`) that avoids the long-held exclusive lock
entirely.

---

### 🛡️ Production Prevention Invariants
1. **Always set `lock_timeout`** before any DDL that could block behind
   long-running queries.
2. **Prefer online schema-change tooling** for large or frequently-migrated
   tables instead of a bare `ALTER TABLE`.
3. **Run migrations during low-traffic windows** and monitor queue depth /
   connection saturation live during the change.
