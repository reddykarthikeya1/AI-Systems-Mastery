"""DEBUG LAB: DB::Exception: Too Many Parts in Table in ClickHouse

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class MergeTreeTable:
    """A toy MergeTree table. Every insert creates a brand-new part; a
    background merge cycle can only reclaim a fixed number of parts, no
    matter how fast the insert rate is."""

    MAX_HEALTHY_PARTS = 300
    MERGE_CYCLE_EVERY_N_INSERTS = 50
    PARTS_RECLAIMED_PER_MERGE_CYCLE = 5

    def __init__(self) -> None:
        self.parts = 0
        self._inserts_since_merge = 0

    def insert_row(self) -> None:
        self.parts += 1  # one single-row HTTP insert == one new on-disk part
        self._inserts_since_merge += 1
        if self._inserts_since_merge >= self.MERGE_CYCLE_EVERY_N_INSERTS:
            self.parts = max(0, self.parts - self.PARTS_RECLAIMED_PER_MERGE_CYCLE)
            self._inserts_since_merge = 0

def reproduce_defect() -> None:
    print("Sending 5,000 single-row HTTP inserts to a MergeTree table...")
    table = MergeTreeTable()
    for _ in range(5000):
        table.insert_row()

    print(f"Parts on disk after 5,000 single-row inserts: {table.parts}")
    print(f"Healthy part-count ceiling: {table.MAX_HEALTHY_PARTS}")
    if table.parts > table.MAX_HEALTHY_PARTS:
        print("[DEFECT OBSERVED] The background merge worker reclaims a fixed "
              "number of parts per cycle, far slower than the single-row insert "
              "rate creates them -- 'Too Many Parts' is now inevitable.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
