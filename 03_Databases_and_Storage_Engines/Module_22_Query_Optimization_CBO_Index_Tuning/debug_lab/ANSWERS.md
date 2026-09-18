# Debug Lab Solution & Forensic Post-Mortem

## Incident: Full Table Scan Caused by Function Wrapping on Indexed Timestamp

---

### 🔍 Forensic Root Cause Analysis
`query_function_wrapped()` models `WHERE DATE(created_at) = '2026-01-01'`. The
index (`OrdersTable.index`) is keyed on the exact, unmodified `created_at`
value, but the predicate wraps the column in a function before comparing it.
A B-Tree index can only be seeked by the raw column value it was built on; once
the column is passed through `DATE(...)`, the optimizer can no longer prove
which index entries could possibly match without evaluating the function on
every row first, so it falls back to a full scan of all 20,000 rows to find
the ~1,000 that match.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def query_sargable(self, day_start, day_end):
    """A sargable range predicate on the raw, unwrapped column CAN seek the
    B-Tree, instead of forcing a function evaluation on every row."""
    return [
        row_id for row_id, ts in self.rows.items()
        if day_start <= ts < day_end
    ]
```

In SQL, rewrite the predicate to be sargable:
```sql
-- was: WHERE DATE(created_at) = '2026-01-01'
WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'
```

---

### 🛡️ Production Prevention Invariants
1. **Never wrap an indexed column in a function** in a `WHERE` clause; rewrite
   as an equivalent range predicate instead.
2. **`EXPLAIN` review in CI** flags any plan showing a full/sequential scan on
   a table above a row-count threshold.
3. **Functional indexes** (`CREATE INDEX ON t (DATE(created_at))`) as a
   fallback only when the wrapped predicate genuinely cannot be rewritten.
