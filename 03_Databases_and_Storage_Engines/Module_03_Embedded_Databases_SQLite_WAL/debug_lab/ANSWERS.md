# Debug Lab Solution & Forensic Post-Mortem

## Incident: Database is Locked Exception on High Concurrent Ingestion

---

### 🔍 Forensic Root Cause Analysis
`MiniSQLiteConnection.busy_timeout_ticks` is `0`. Any writer that arrives while
another connection holds the write lock has zero ticks of grace to wait, so it
raises `LockedError` ("database is locked") on the very first contention it
meets, instead of quietly retrying until the lock clears -- exactly what
happens when `PRAGMA busy_timeout` is never configured on a real SQLite
connection under `SQLITE_BUSY`.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class MiniSQLiteConnection:
    busy_timeout_ticks = 5000   # PRAGMA busy_timeout = 5000 (milliseconds)

    def write(self, writer_id, arrival_tick, lock_release_tick):
        if arrival_tick + self.busy_timeout_ticks < lock_release_tick:
            raise LockedError(f"writer {writer_id}: database is locked")
        return True   # waited out the lock instead of failing immediately
```

In real SQLite: `conn.execute("PRAGMA busy_timeout = 5000")` right after opening
every connection that might write.

---

### 🛡️ Production Prevention Invariants
1. **Set `busy_timeout` on every connection** as part of a shared connection
   factory, so no call site can forget it.
2. **WAL mode + a single writer queue** for high-concurrency ingestion paths.
3. **Chaos testing:** inject deliberate lock contention in CI and assert the
   write success rate stays at 100% within the configured timeout.
