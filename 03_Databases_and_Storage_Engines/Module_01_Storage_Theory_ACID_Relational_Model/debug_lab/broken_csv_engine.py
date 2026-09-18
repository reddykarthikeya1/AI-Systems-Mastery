"""DEBUG LAB: Uncommitted Transaction Leaks into Primary Table During Power Failure

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class MiniTable:
    """A toy storage engine: an in-memory 'primary table' plus a transaction buffer."""

    def __init__(self) -> None:
        self.primary_rows: list[dict] = []   # durable, committed data (table.csv)
        self._pending: list[dict] = []
        self._in_transaction = False

    def begin(self) -> None:
        self._in_transaction = True
        self._pending = []

    def insert(self, row: dict) -> None:
        if not self._in_transaction:
            self.primary_rows.append(row)
            return
        self._pending.append(row)
        self.primary_rows.append(row)

    def commit(self) -> None:
        self._pending = []
        self._in_transaction = False

    def crash_before_commit(self) -> None:
        """Simulates a power failure: the process dies before COMMIT ever runs."""
        self._pending = []
        self._in_transaction = False

def reproduce_defect() -> None:
    print("Simulating an ingestion transaction interrupted by a power failure...")
    table = MiniTable()
    table.insert({"id": 1, "balance": 100})  # durable baseline row, no transaction open

    table.begin()
    table.insert({"id": 2, "balance": 9999})  # written only inside an open transaction
    table.crash_before_commit()               # power lost: COMMIT never ran

    persisted_ids = sorted(r["id"] for r in table.primary_rows)
    expected_ids = [1]  # only committed data should have survived the crash

    print(f"Rows visible in table.csv after restart: {persisted_ids}")
    print(f"Rows expected to be visible:              {expected_ids}")
    if persisted_ids != expected_ids:
        print("[DEFECT OBSERVED] Row id=2 was never committed, yet it survived the "
              "crash and is now permanently in the primary table.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
