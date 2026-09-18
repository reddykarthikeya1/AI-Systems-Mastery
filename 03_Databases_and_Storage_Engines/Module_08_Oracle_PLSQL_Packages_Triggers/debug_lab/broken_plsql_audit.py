"""DEBUG LAB: Audit Log Erased When Financial Transaction Fails

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class TransferLedger:
    """A toy ledger where audit logging happens inside the same transaction as the transfer it audits."""

    def __init__(self) -> None:
        self.committed_balances: dict[str, int] = {}
        self.committed_audit_log: list[str] = []
        self._tx_balances: dict[str, int] | None = None
        self._tx_audit: list[str] | None = None

    def begin(self) -> None:
        self._tx_balances = dict(self.committed_balances)
        self._tx_audit = list(self.committed_audit_log)

    def transfer(self, src: str, dst: str, amount: int) -> None:
        assert self._tx_balances is not None and self._tx_audit is not None
        if self._tx_balances[src] < amount:
            self._tx_audit.append(f"DENIED transfer {src}->{dst} amount={amount}")
            raise ValueError("insufficient funds")
        self._tx_balances[src] -= amount
        self._tx_balances[dst] += amount
        self._tx_audit.append(f"OK transfer {src}->{dst} amount={amount}")

    def commit(self) -> None:
        self.committed_balances = self._tx_balances  # type: ignore[assignment]
        self.committed_audit_log = self._tx_audit  # type: ignore[assignment]

    def rollback(self) -> None:
        self._tx_balances = None
        self._tx_audit = None  # the DENIED entry recorded this transaction vanishes too

def reproduce_defect() -> None:
    print("Attempting a transfer that exceeds the available balance...")
    ledger = TransferLedger()
    ledger.committed_balances = {"acct_A": 10, "acct_B": 0}

    ledger.begin()
    try:
        ledger.transfer("acct_A", "acct_B", 100)
    except ValueError:
        ledger.rollback()

    audit_count = len(ledger.committed_audit_log)
    print(f"Audit log entries after the declined transfer: {audit_count}")
    print(f"Audit log entries expected (security requires the denial be recorded): 1")
    if audit_count == 0:
        print("[DEFECT OBSERVED] The DENIED audit entry was rolled back along with "
              "the failed transfer -- there is no record this was ever attempted.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
