# Debug Lab Solution & Forensic Post-Mortem

## Incident: ORA-04031 Shared Pool Out of Memory via Literal SQL

---

### 🔍 Forensic Root Cause Analysis
`parse_literal()` builds SQL text with the literal value baked directly into
the string (`f"SELECT * FROM emp WHERE id = {emp_id}"`). Every distinct
`emp_id` produces a byte-for-byte different SQL string, so the shared pool
cannot recognize any two calls as "the same statement" -- each one is hard
parsed and cached separately, evicting older entries once the pool fills.
5,000 lookups against a 1,000-slot pool means the pool is constantly
thrashing, which in real Oracle manifests as library cache contention and,
under memory pressure, ORA-04031.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def parse_bind(self, emp_id):
    sql = "SELECT * FROM emp WHERE id = :emp_id"   # one statement, bound at execute time
    self._store(sql)
```

In application code: always use bind variables (`:emp_id`) instead of string-
interpolating literals into SQL text, so the same cursor is shared and reused
across every call regardless of which `emp_id` is requested.

---

### 🛡️ Production Prevention Invariants
1. **Ban string-interpolated SQL** in code review and static analysis for any
   value that varies per call.
2. **`CURSOR_SHARING = FORCE`** as a safety net for legacy code that cannot be
   changed immediately (with awareness of its own trade-offs).
3. **Monitor `v$librarycache` reload/hit ratios** and alert on hard-parse rate
   spikes.
