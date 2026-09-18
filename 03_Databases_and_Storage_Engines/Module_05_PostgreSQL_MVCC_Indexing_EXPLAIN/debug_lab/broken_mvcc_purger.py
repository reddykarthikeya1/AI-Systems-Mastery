"""DEBUG LAB: Dead Tuple Bloat Prevents Autovacuum Reclamation

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class MiniMVCCTable:
    """A toy MVCC table: tuples carry xmin/xmax, vacuum reclaims dead ones."""

    def __init__(self) -> None:
        self.tuples: list[dict] = []
        self.active_txns: dict[int, int] = {}  # txn_id -> its xmin snapshot
        self._next_xid = 1

    def begin(self) -> int:
        xid = self._next_xid
        self._next_xid += 1
        self.active_txns[xid] = xid
        return xid

    def commit(self, xid: int) -> None:
        self.active_txns.pop(xid, None)

    def insert(self, row_id: int, xid: int) -> None:
        self.tuples.append({"id": row_id, "xmin": xid, "xmax": None})

    def delete(self, row_id: int, xid: int) -> None:
        for t in self.tuples:
            if t["id"] == row_id and t["xmax"] is None:
                t["xmax"] = xid

    def vacuum(self) -> int:
        floor = min(self.active_txns.values()) if self.active_txns else self._next_xid
        before = len(self.tuples)
        self.tuples = [t for t in self.tuples if t["xmax"] is None or t["xmax"] >= floor]
        return before - len(self.tuples)

def reproduce_defect() -> None:
    print("Running a long reporting query alongside routine inserts and deletes...")
    table = MiniMVCCTable()
    idle_reporting_txn = table.begin()  # "BEGIN; SELECT ..." -- left open for hours

    for row_id in range(50):
        xid = table.begin(); table.insert(row_id, xid); table.commit(xid)
    for row_id in range(25):
        xid = table.begin(); table.delete(row_id, xid); table.commit(xid)

    reclaimed = table.vacuum()
    print(f"Dead tuples reclaimed by vacuum: {reclaimed} (expected: 25)")
    if reclaimed < 25:
        print("[DEFECT OBSERVED] The idle reporting transaction is still pinning an "
              "old xmin, so autovacuum cannot reclaim any of the 25 dead tuples.")
    else:
        print("No defect observed.")
    table.commit(idle_reporting_txn)

if __name__ == "__main__":
    reproduce_defect()
