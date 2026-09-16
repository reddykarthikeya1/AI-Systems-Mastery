# Debug Lab Solution & Forensic Post-Mortem

## Incident: Accounting Discrepancy from Unbalanced Double-Entry Ledger Posting

---

### 🔍 Forensic Root Cause Analysis
Financial ledgers must balance to the exact cent across every posting. Allowing unbalanced postings corrupts total balance sheets.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Enforce immutable double-entry ledger invariants:
# total_debits = sum(p.amount for p in postings if p.type == 'DEBIT')
# total_credits = sum(p.amount for p in postings if p.type == 'CREDIT')
# if total_debits != total_credits:
#     raise AccountingDiscrepancyException('Posting unbalanced!')

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
