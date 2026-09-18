# Debug Lab Solution & Forensic Post-Mortem

## Incident: Distributed Lock Race Condition Releases Another Worker's Lock

---

### 🔍 Forensic Root Cause Analysis
`RedisLike.delete()` is an unconditional `DEL` -- it removes whatever value is
currently stored at the key without checking who put it there. Worker 1's job
ran longer than the lock's TTL, so the lock already expired and was
legitimately re-acquired by worker 2. When worker 1 finally finishes and calls
`DEL` believing it is releasing its own lock, it actually deletes worker 2's
active lock, letting a third worker acquire it while worker 2 is still mid-flight.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def delete_if_owner(self, key, token):
    """Equivalent to Redis's compare-and-delete Lua script: only release the
    lock if the caller's token still matches the value stored at the key."""
    current = self.store.get(key)
    if current is not None and current[0] == token:
        self.store.pop(key, None)
        return True
    return False   # someone else now owns this lock -- do NOT touch it
```

Each worker must release the lock with its own unique token, via an atomic
compare-and-delete (in real Redis, a Lua script using `GET` + `DEL`), never a
bare `DEL`.

---

### 🛡️ Production Prevention Invariants
1. **Fencing tokens / ownership tokens** on every distributed lock; releases
   must be conditional on token match, implemented atomically.
2. **TTL >> expected critical-section duration**, with periodic lock renewal
   (heartbeat/extend) for long-running work instead of a single fixed TTL.
3. **Idempotent downstream work**, so a lock race that does slip through
   cannot corrupt state.
