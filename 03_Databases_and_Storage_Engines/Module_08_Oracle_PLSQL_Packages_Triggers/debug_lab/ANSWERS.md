# Debug Lab Solution & Forensic Post-Mortem

## Incident: Audit Log Erased When Financial Transaction Fails

---

### 🔍 Forensic Root Cause Analysis
`TransferLedger.transfer()` appends the `DENIED ...` audit entry into
`self._tx_audit`, the same in-flight transaction state that holds the balance
changes. When the caller calls `rollback()`, both `_tx_balances` and
`_tx_audit` are discarded together -- the audit record has no existence
independent of the transaction it is supposed to be witnessing, so a rolled
back transfer leaves zero evidence it was ever attempted.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class TransferLedger:
    def __init__(self):
        ...
        self.committed_audit_log = []   # audit writes commit independently, immediately

    def transfer(self, src, dst, amount):
        if self._tx_balances[src] < amount:
            self.committed_audit_log.append(f"DENIED transfer {src}->{dst} amount={amount}")
            raise ValueError("insufficient funds")
        ...
```

In PL/SQL, the equivalent fix is `PRAGMA AUTONOMOUS_TRANSACTION` on the audit
logging procedure, with its own explicit `COMMIT`, so the audit write survives
regardless of what the calling transaction later does.

---

### 🛡️ Production Prevention Invariants
1. **Audit trails must be autonomous** (or written to an append-only external
   system) -- never dependent on the outcome of the transaction they audit.
2. **Test the failure path explicitly:** every audited operation needs a test
   that forces a rollback and asserts the audit entry still exists.
3. **Compliance review** for any audit log whose durability depends on
   application-transaction boundaries.
