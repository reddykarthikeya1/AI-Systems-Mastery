# Debug Lab Solution & Forensic Post-Mortem

## Incident: DB::Exception: Too Many Parts in Table in ClickHouse

---

### 🔍 Forensic Root Cause Analysis
`insert_row()` creates one brand-new on-disk part per call -- the direct
consequence of sending 5,000 single-row HTTP inserts per second to a
MergeTree table instead of batching them. The background merge cycle only
reclaims a fixed number of parts (`PARTS_RECLAIMED_PER_MERGE_CYCLE`) each time
it runs, a rate far below the insert rate, so the part count grows without
bound and quickly blows past the healthy ceiling ClickHouse enforces before
raising "Too Many Parts".

---

### 🛠️ Production Corrective Action & Code Fix

```python
class BatchingMergeTreeWriter:
    """Buffers rows client-side and flushes in large batches, so one insert
    creates one part covering thousands of rows instead of one row each."""

    BATCH_SIZE = 5000

    def __init__(self, table):
        self.table = table
        self.buffer = []

    def insert_row(self, row):
        self.buffer.append(row)
        if len(self.buffer) >= self.BATCH_SIZE:
            self.table.insert_batch(self.buffer)   # ONE part for the whole batch
            self.buffer = []
```

In production: insert through a buffering layer (or ClickHouse's own
`async_insert`) so each physical INSERT covers thousands of rows, not one.

---

### 🛡️ Production Prevention Invariants
1. **Never send single-row inserts to MergeTree tables** at high frequency;
   batch client-side or enable `async_insert`.
2. **Monitor `system.parts` count per table** and alert well before the
   configured `parts_to_throw_insert` limit.
3. **Load-test ingestion paths at production insert rates**, not just
   correctness-test volumes.
