"""DEBUG LAB: Full Table Scan Caused by Function Wrapping on Indexed Timestamp

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class OrdersTable:
    """A toy table with a real B-Tree index on the raw created_at column."""

    def __init__(self) -> None:
        self.rows: dict[int, str] = {}       # row_id -> "YYYY-MM-DD HH:MM:SS"
        self.index: dict[str, int] = {}      # exact timestamp -> row_id

    def insert(self, row_id: int, timestamp: str) -> None:
        self.rows[row_id] = timestamp
        self.index[timestamp] = row_id

    def query_function_wrapped(self, target_date: str) -> tuple[list[int], int]:
        """WHERE DATE(created_at) = target_date -- wrapping the column in a
        function means the planner can no longer seek the B-Tree by prefix."""
        matches, scanned = [], 0
        for row_id, timestamp in self.rows.items():
            scanned += 1
            if timestamp.startswith(target_date):
                matches.append(row_id)
        return matches, scanned

def reproduce_defect() -> None:
    print("Filtering 20,000 orders for DATE(created_at) = '2026-01-01'...")
    table = OrdersTable()
    dates = [f"2025-{month:02d}-{day:02d}" for month in range(1, 11) for day in (1, 15)]
    dates.append("2026-01-01")  # the target date, one slice among 21 distinct dates
    for row_id in range(20000):
        table.insert(row_id, f"{dates[row_id % len(dates)]} 12:00:00")

    matches, scanned = table.query_function_wrapped("2026-01-01")
    print(f"Rows scanned to answer the filter: {scanned}")
    print(f"Rows actually matching that date: {len(matches)}")
    if scanned > len(matches) * 10:
        print("[DEFECT OBSERVED] Wrapping created_at in DATE() blinds the planner "
              "to the B-Tree index, forcing a full scan of all 20,000 rows to "
              "find the handful that match.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
