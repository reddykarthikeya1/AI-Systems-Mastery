# Debug Lab Solution & Forensic Post-Mortem

## Incident: Uncommitted Transaction Leaks into Primary Table During Power Failure

---

### 🔍 Forensic Root Cause Analysis
`MiniTable.insert()` appends every row straight into `primary_rows` (the durable
table) the moment it is called, whether or not a transaction is open. The
`_pending` buffer is filled too, but nothing ever actually gates what reaches
the primary table on `_pending`. When the process is killed before `commit()`
runs, whatever was already appended to `primary_rows` is already "on disk" and
survives the crash, even though it was never committed.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def insert(self, row: dict) -> None:
    if not self._in_transaction:
        self.primary_rows.append(row)
        return
    self._pending.append(row)   # buffered only -- NOT written to primary_rows yet

def commit(self) -> None:
    self.primary_rows.extend(self._pending)   # durable write happens here, and only here
    self._pending = []
    self._in_transaction = False
```

A crash before `commit()` now simply discards `_pending`; `primary_rows` never
saw the uncommitted data in the first place.

---

### 🛡️ Production Prevention Invariants
1. **Write-ahead discipline:** durable state must only change inside `commit()`,
   never inside `insert()`/`update()`/`delete()`.
2. **Crash-injection tests:** every storage engine test suite should kill the
   process mid-transaction and assert the durable store is unchanged.
3. **Fail-Safe Defaults:** an interrupted transaction must always be equivalent
   to it never having started.
