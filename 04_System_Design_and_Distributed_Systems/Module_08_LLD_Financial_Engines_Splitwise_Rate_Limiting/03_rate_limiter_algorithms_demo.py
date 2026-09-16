#!/usr/bin/env python3
"""Module 08 Demo: Live Splitwise Debt Simplification & Rate Limiter."""

import sys
import time
from decimal import Decimal
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from splitwise_engine import (
    Split,
    SplitType,
    SplitwiseLedger,
    TokenBucketRateLimiter,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 08: SPLITWISE DEBT SIMPLIFICATION & RATE LIMITING DEMO")
    print("=" * 72)

    # 1. Splitwise Demo
    print("\n--- 1. Splitwise Expense Sharing & Transitive Debt Simplification ---")
    ledger = SplitwiseLedger()

    # Dinner: Alice pays $120 for Alice, Bob, Charlie, David ($30 each)
    ledger.add_expense(
        paid_by="Alice",
        total_amount=Decimal("120.00"),
        split_type=SplitType.EQUAL,
        participants=["Alice", "Bob", "Charlie", "David"],
    )

    # Taxi: Bob pays $60 for Bob & Charlie ($30 each)
    ledger.add_expense(
        paid_by="Bob",
        total_amount=Decimal("60.00"),
        split_type=SplitType.EXACT,
        splits=[Split("Bob", Decimal("30.00")), Split("Charlie", Decimal("30.00"))],
    )

    print("Net Balances Before Simplification:")
    for user, bal in ledger.net_balances.items():
        status = f"gets back ${bal}" if bal > 0 else f"owes ${abs(bal)}"
        print(f"  {user:<10}: {status}")

    print("\nOptimized Settlement Transactions (Min Cash Flow Algorithm):")
    transactions = ledger.simplify_debts()
    for tx in transactions:
        print(f"  -> {tx.debtor:<8} pays {tx.creditor:<8} ${tx.amount}")

    # 2. Token Bucket Rate Limiter
    print("\n--- 2. Token Bucket Rate Limiter Simulation ---")
    limiter = TokenBucketRateLimiter(capacity=4, refill_rate=2.0)
    print("Config: Capacity = 4 tokens, Refill = 2 tokens/sec")

    print("\nSending burst of 6 rapid requests:")
    for i in range(1, 7):
        allowed = limiter.allow_request()
        status = "ALLOWED (200 OK)" if allowed else "REJECTED (429 Too Many Requests)"
        print(f"  Request #{i}: {status} (remaining: {limiter.current_tokens:.1f})")

    print("\nSleeping 1.0s to allow token replenishment...")
    time.sleep(1.0)
    print(f"Tokens after 1s refill: {limiter.current_tokens:.1f}")

    print("Sending 2 more requests:")
    for i in range(7, 9):
        allowed = limiter.allow_request()
        status = "ALLOWED (200 OK)" if allowed else "REJECTED (429)"
        print(f"  Request #{i}: {status}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
