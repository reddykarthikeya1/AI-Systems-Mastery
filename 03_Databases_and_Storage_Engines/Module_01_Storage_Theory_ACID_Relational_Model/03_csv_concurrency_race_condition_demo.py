"""Module 01 Demo 01: Demonstrating CSV Concurrency Race Conditions and Data Loss.

This script simulates what happens when multiple concurrent threads attempt to
update a flat CSV file without DBMS concurrency controls or locking mechanisms.
"""

from __future__ import annotations

import csv
import threading
import time
from pathlib import Path

DATA_FILE = Path(__file__).parent / "bank_accounts.csv"


def reset_csv():
    """Initializes the CSV with an opening balance of 1,000 for Alice."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["account_id", "owner", "balance"])
        writer.writerow(["1", "Alice", "1000.0"])


def withdraw_unsafe(account_id: str, amount: float):
    """Simulates an unsafe read-modify-write cycle on a flat CSV file."""
    # 1. Read the current balance
    rows = []
    current_balance = 0.0
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["account_id"] == account_id:
                current_balance = float(row["balance"])
            rows.append(row)

    # 2. Simulate artificial processing/network latency
    time.sleep(0.01)

    # 3. Calculate new balance
    new_balance = current_balance - amount

    # 4. Overwrite file with updated balance
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["account_id", "owner", "balance"])
        writer.writeheader()
        for row in rows:
            if row["account_id"] == account_id:
                row["balance"] = str(new_balance)
            writer.writerow(row)


def main():
    print("=== Module 01 Demo 01: Unsafe Flat File Concurrency Test ===")
    reset_csv()
    print("Initial balance for Alice: $1,000.00")
    print("Launching 10 concurrent threads, each withdrawing $50.00...")

    threads = []
    for _ in range(10):
        t = threading.Thread(target=withdraw_unsafe, args=("1", 50.0))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Read final balance
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["account_id"] == "1":
                final_balance = float(row["balance"])

    print("Expected final balance: $500.00 (1000 - 10 * 50)")
    print(f"ACTUAL final balance:   ${final_balance:.2f}")

    if final_balance > 500.0:
        print("🚨 CATASTROPHIC FAILURE: Lost updates detected! Flat files lack ACID isolation.")
    else:
        print("Surprising success! (Run multiple times to observe thread interleaving).")

    # Clean up demo file
    if DATA_FILE.exists():
        DATA_FILE.unlink()


if __name__ == "__main__":
    main()
