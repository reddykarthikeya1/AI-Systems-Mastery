# Debug Lab Solution & Forensic Post-Mortem

## Incident: Dual-Write Inconsistency: Database Committed but Message Broker Publish Failed

---

### 🔍 Forensic Root Cause Analysis
Writing to a database and a message broker in sequence cannot be made atomic without distributed transactions. Network crashes between step 1 and step 2 leave systems out of sync.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Implement the Transactional Outbox Pattern:
# Save domain entity AND outbox message into the SAME database transaction:
# BEGIN;
#   INSERT INTO orders ...;
#   INSERT INTO outbox_table (payload, status) VALUES (..., 'PENDING');
# COMMIT;
# A separate relay process reads outbox_table and publishes to Kafka with retry!

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
