# Debug Lab Solution & Forensic Post-Mortem

## Incident: ReadFailure Scanned Over 100,000 Tombstones

---

### 🔍 Forensic Root Cause Analysis
`WideRow.delete()` marks a cell with a tombstone marker rather than physically
removing it; the underlying storage still has to keep and later compact away
that marker. The polling loop calls `write()` immediately followed by
`delete()` for every consumed queue item, so the partition accumulates one
tombstone per processed item forever. `read_range()` must walk every cell,
live or dead, in insertion order to assemble its result -- so returning 5 live
rows out of a partition holding 20,000 processed-and-deleted items means
scanning all 20,005 cells.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class TTLQueueRow:
    """Processed items expire via TTL instead of an explicit per-item DELETE,
    so Cassandra reclaims them automatically during compaction without ever
    generating a tombstone the application has to scan past."""

    def write_with_ttl(self, column, value, ttl_seconds):
        self.cells[column] = (value, ttl_seconds)   # no DELETE call needed at all
```

In CQL: `INSERT INTO queue (...) VALUES (...) USING TTL 3600;` instead of an
explicit `DELETE` per consumed row, paired with a lower `gc_grace_seconds` and
regular compaction so expired data is purged promptly.

---

### 🛡️ Production Prevention Invariants
1. **Prefer TTL over explicit per-row DELETE** for high-volume queue/expiry
   workloads in Cassandra.
2. **Monitor `tombstone_warn_threshold` / `tombstone_failure_threshold`** and
   alert well before reads start failing.
3. **Avoid CQL `DELETE` in tight polling loops**; batch and compact instead.
