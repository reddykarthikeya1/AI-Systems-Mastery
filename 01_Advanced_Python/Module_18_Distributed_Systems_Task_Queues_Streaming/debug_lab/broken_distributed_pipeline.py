#!/usr/bin/env python3
"""Broken Distributed Task Consumer demonstrating non-idempotent redelivery traps."""

processed_transfers: list[str] = []

def process_bank_transfer(transfer_id: str, amount: float, balances: dict[str, float]):
    # If the broker redelivers the message due to an ACK network timeout,
    # the balance is debited twice!
    balances["alice"] -= amount
    balances["bob"] += amount
    processed_transfers.append(transfer_id)

if __name__ == "__main__":
    balances = {"alice": 1000.0, "bob": 200.0}
    tx_id = "TX-888"

    # First attempt
    process_bank_transfer(tx_id, 100.0, balances)
    # Broker redeliver simulation:
    process_bank_transfer(tx_id, 100.0, balances)

    print(f"Alice balance after redelivery: {balances['alice']} (Expected 900.0, got 800.0 due to double-charge!)")
