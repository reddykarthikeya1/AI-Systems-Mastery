"""DEBUG LAB: Deadlock 1213 on High Concurrency Multi-Row Updates

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class LockManager:
    """A toy row-lock manager with wait-for-graph deadlock detection."""

    def __init__(self) -> None:
        self.held: dict[int, str] = {}          # row_id -> txn holding it
        self.waiting_for: dict[str, int] = {}    # txn -> row_id it wants

    def acquire(self, txn: str, row_id: int) -> bool:
        holder = self.held.get(row_id)
        if holder is None or holder == txn:
            self.held[row_id] = txn
            self.waiting_for.pop(txn, None)
            return True
        self.waiting_for[txn] = row_id
        return False

    def has_cycle(self) -> bool:
        for start in self.waiting_for:
            cur, seen = start, set()
            while cur in self.waiting_for:
                holder = self.held.get(self.waiting_for[cur])
                if holder is None or holder in seen:
                    break
                if holder == start:
                    return True
                seen.add(holder)
                cur = holder
        return False

def reproduce_defect() -> None:
    print("Two threads update the same inventory rows in opposite order...")
    locks = LockManager()

    # Thread A updates item 10 then item 20; Thread B updates item 20 then item 10.
    locks.acquire("txn_A", 10)
    locks.acquire("txn_B", 20)
    locks.acquire("txn_A", 20)  # blocks: held by txn_B
    locks.acquire("txn_B", 10)  # blocks: held by txn_A -- cycle now exists

    deadlocked = locks.has_cycle()
    print(f"Deadlock (cyclic wait) detected: {deadlocked}")
    print(f"Deadlocks expected with consistent lock ordering: False")
    if deadlocked:
        print("[DEFECT OBSERVED] ER_LOCK_DEADLOCK (1213): txn_B must be rolled back "
              "because the two threads acquire item locks in inconsistent order.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
