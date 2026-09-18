"""DEBUG LAB: ReadFailure Scanned Over 100,000 Tombstones

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

_TOMBSTONE = object()

class WideRow:
    """A toy Cassandra partition. DELETE writes a tombstone marker rather than
    physically removing the cell, so a range read must still walk past it."""

    def __init__(self) -> None:
        self.cells: dict[str, object] = {}

    def write(self, column: str, value: str) -> None:
        self.cells[column] = value

    def delete(self, column: str) -> None:
        self.cells[column] = _TOMBSTONE

    def read_range(self) -> tuple[list[str], int]:
        scanned = 0
        live = []
        for column, value in self.cells.items():
            scanned += 1
            if value is not _TOMBSTONE:
                live.append(column)
        return live, scanned

def reproduce_defect() -> None:
    print("Polling a queue partition: consume-then-DELETE, 20,000 times...")
    row = WideRow()
    for i in range(20000):
        column = f"item-{i}"
        row.write(column, "payload")
        row.delete(column)  # consumed items are deleted immediately, in a hot loop
    for i in range(5):
        row.write(f"pending-{i}", "payload")  # a handful of items still awaiting pickup

    live, scanned = row.read_range()
    print(f"Live rows returned: {len(live)}")
    print(f"Cells scanned to produce them: {scanned}")
    if scanned > len(live) * 100:
        print("[DEFECT OBSERVED] The reader scanned 20,000+ tombstones to return "
              "5 live rows -- the poll-and-DELETE pattern is choking range reads.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
