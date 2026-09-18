# Debug Lab Solution & Forensic Post-Mortem

## Incident: Dead Tuple Bloat Prevents Autovacuum Reclamation

---

### 🔍 Forensic Root Cause Analysis
`idle_reporting_txn` calls `begin()` and is never committed. `vacuum()` can
only reclaim a dead tuple once its `xmax` is older than the oldest `xmin` of
any still-active transaction (`oldest_active_xmin()`), because MVCC must keep
a dead row visible to any snapshot that started before it was deleted. Since
the idle transaction's `xmin` is the very first one issued, `oldest_active_xmin()`
never advances past it, so every tuple deleted after it -- no matter how long
ago -- is permanently ineligible for reclamation until that transaction ends.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def reproduce_fixed():
    table = MiniMVCCTable()
    idle = table.begin()
    table.commit(idle)          # <-- the fix: never leave a transaction open and idle

    for row_id in range(50):
        xid = table.begin(); table.insert(row_id, xid); table.commit(xid)
    for row_id in range(25):
        xid = table.begin(); table.delete(row_id, xid); table.commit(xid)

    reclaimed = table.vacuum()  # now reclaims all 25 dead tuples
```

In production Postgres: kill or timebox any session showing `idle in
transaction` for longer than a few minutes (`idle_in_transaction_session_timeout`).

---

### 🛡️ Production Prevention Invariants
1. **`idle_in_transaction_session_timeout`** set on every role that can run ad
   hoc reporting queries.
2. **Alert on `pg_stat_activity.xact_start` age** exceeding a threshold for any
   connection.
3. **`autovacuum` monitoring:** alert when a table's dead-tuple count grows
   without `last_autovacuum` advancing.
