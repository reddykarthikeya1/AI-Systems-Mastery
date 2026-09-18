"""DEBUG LAB: Running Total Generates Identical Duplicate Numbers on Duplicate Dates

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

def running_total(rows: list[tuple[str, int]]) -> list[int]:
    """Computes SUM(amount) OVER (ORDER BY sale_date) using the default frame.

    Every row with the same ORDER BY key is a "peer". The default frame is
    RANGE, which includes all peers of the current row, so every row sharing
    a date ends up seeing the exact same cumulative total.
    """
    totals = []
    running = 0
    i, n = 0, len(rows)
    while i < n:
        date = rows[i][0]
        j = i
        peer_sum = 0
        while j < n and rows[j][0] == date:
            peer_sum += rows[j][1]
            j += 1
        running += peer_sum
        for _ in range(i, j):
            totals.append(running)  # every peer row reports the same final total
        i = j
    return totals

def reproduce_defect() -> None:
    print("Computing a running total over daily sales with two same-day orders...")
    sales = [
        ("2026-01-01", 100),
        ("2026-01-02", 50),
        ("2026-01-02", 30),  # duplicate date
        ("2026-01-03", 20),
    ]
    actual = running_total(sales)
    expected = [100, 150, 180, 200]  # each row's running total should strictly increase

    print(f"Actual running totals:   {actual}")
    print(f"Expected running totals: {expected}")
    if actual != expected:
        print("[DEFECT OBSERVED] Both 2026-01-02 rows report the identical running "
              "total of 180 instead of two distinct, increasing values.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
