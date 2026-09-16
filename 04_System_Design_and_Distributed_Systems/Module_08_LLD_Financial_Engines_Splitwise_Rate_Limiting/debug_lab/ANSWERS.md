# Debug Lab Solution & Forensic Post-Mortem

## Incident: Penny Discrepancy Leak in Three-Way Bill Split

---

### 🔍 Forensic Root Cause Analysis
Dividing $100.00 by 3 gives 33.3333... Rounding each to $33.33 results in $99.99 total, leaking 1 cent into financial limbo.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def split_bill_exact(total_cents: int, people: list[str]) -> dict[str, int]:
    n = len(people)
    base = total_cents // n
    remainder = total_cents % n
    result = {}
    for i, p in enumerate(people):
        result[p] = base + (1 if i < remainder else 0)
    return result  # Guarantees sum(result.values()) == total_cents down to the exact penny!

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
