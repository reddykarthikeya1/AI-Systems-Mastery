"""Module 01 Demo 02: Write-Ahead Logging (WAL) and Crash Recovery Simulation.

Demonstrates how appending transaction intentions to an immutable WAL on disk
guarantees Atomicity and Durability even if the process crashes midway.
"""

from __future__ import annotations

import json
from pathlib import Path

WAL_FILE = Path(__file__).parent / "demo_wal.log"
DATABASE_FILE = Path(__file__).parent / "demo_db.json"


def write_ahead_log(tx_id: int, action: str, details: dict):
    """Appends transaction intent to the WAL before applying it to the database."""
    entry = {"tx_id": tx_id, "action": action, "details": details}
    with open(WAL_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def simulate_transaction(tx_id: int, sender: str, receiver: str, amount: float, crash_midway: bool = False):
    """Executes a transaction using WAL mechanics."""
    print(f"\n--- Starting Transaction #{tx_id}: Transfer ${amount} from {sender} to {receiver} ---")

    # 1. Log transaction BEGIN
    write_ahead_log(tx_id, "BEGIN", {})
    print("1. Logged [BEGIN] to WAL.")

    # 2. Log transfer details
    write_ahead_log(tx_id, "DEBIT", {"account": sender, "amount": amount})
    print(f"2. Logged [DEBIT ${amount} from {sender}] to WAL.")

    if crash_midway:
        print("💥 POWER OUTAGE SIMULATED! Process crashed before COMMIT was reached!")
        return False

    write_ahead_log(tx_id, "CREDIT", {"account": receiver, "amount": amount})
    print(f"3. Logged [CREDIT ${amount} to {receiver}] to WAL.")

    # 3. Log COMMIT
    write_ahead_log(tx_id, "COMMIT", {})
    print("4. Logged [COMMIT] to WAL. Transaction is now DURABLE.")
    return True


def recover_from_crash():
    """Reads WAL on startup and rolls back uncommitted transactions (ARIES-style recovery)."""
    print("\n--- Running Crash Recovery from WAL ---")
    if not WAL_FILE.exists():
        print("No WAL found; database is clean.")
        return

    transactions: dict[int, list[dict]] = {}
    committed_txs: set[int] = set()

    with open(WAL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            tx_id = entry["tx_id"]
            if tx_id not in transactions:
                transactions[tx_id] = []
            transactions[tx_id].append(entry)
            if entry["action"] == "COMMIT":
                committed_txs.add(tx_id)

    print(f"Detected {len(transactions)} total transactions in WAL.")
    print(f"Committed transactions: {sorted(committed_txs)}")

    for tx_id, actions in transactions.items():
        if tx_id in committed_txs:
            print(f"✅ Tx #{tx_id}: Fully committed. Data safely retained.")
        else:
            print(f"🛑 Tx #{tx_id}: INCOMPLETE / CRASHED! Rolling back actions to protect Atomicity.")

    # Clean up demo files
    if WAL_FILE.exists():
        WAL_FILE.unlink()


def main():
    print("=== Module 01 Demo 02: Write-Ahead Log (WAL) Crash Recovery ===")
    if WAL_FILE.exists():
        WAL_FILE.unlink()

    # Tx 1: Successful commit
    simulate_transaction(tx_id=1, sender="Alice", receiver="Bob", amount=100.0, crash_midway=False)

    # Tx 2: Crashed halfway through
    simulate_transaction(tx_id=2, sender="Charlie", receiver="Dana", amount=500.0, crash_midway=True)

    # Recovery phase
    recover_from_crash()


if __name__ == "__main__":
    main()
