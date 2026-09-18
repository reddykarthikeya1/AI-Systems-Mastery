# Debug Lab Solution & Forensic Post-Mortem

## Incident: Deadlock 1213 on High Concurrency Multi-Row Updates

---

### 🔍 Forensic Root Cause Analysis
`txn_A` locks item 10 then requests item 20; `txn_B` locks item 20 then
requests item 10. Neither transaction can proceed and neither will release
what it already holds, so InnoDB's wait-for graph forms a cycle -- a classic
deadlock caused purely by the two code paths acquiring the same two row locks
in opposite order. This is a property of lock *acquisition order*, not of the
data itself.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def update_inventory(locks, txn, item_ids):
    for item_id in sorted(item_ids):   # <-- always acquire locks in a fixed, global order
        locks.acquire(txn, item_id)
```

Applied to the reproduction: both `txn_A` and `txn_B` update `sorted([10, 20])`,
i.e. item 10 before item 20, regardless of which thread they run on. No cycle
can form because both transactions request the same first lock before either
requests the second.

---

### 🛡️ Production Prevention Invariants
1. **Canonical lock ordering:** any code path that locks more than one row in
   the same statement/transaction must sort keys first.
2. **`innodb_deadlock_detect` + retry logic:** treat error 1213 as retryable
   with exponential backoff, never as a hard failure surfaced to the user.
3. **Load-test with adversarial interleavings** before shipping any
   multi-row update path.
