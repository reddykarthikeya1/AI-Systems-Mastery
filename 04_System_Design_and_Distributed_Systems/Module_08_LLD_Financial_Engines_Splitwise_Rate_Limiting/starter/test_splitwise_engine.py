"""Unit tests for Splitwise Engine & Token Bucket Rate Limiter."""

from __future__ import annotations

import time
from decimal import Decimal

from splitwise_engine import (
    Split,
    SplitType,
    SplitwiseLedger,
    TokenBucketRateLimiter,
)


def test_splitwise_equal_split_and_penny_rounding() -> None:
    ledger = SplitwiseLedger()
    # $100 split 3 ways: 33.33 + 33.33 + 33.34 = 100.00
    ledger.add_expense(
        paid_by="Alice",
        total_amount=Decimal("100.00"),
        split_type=SplitType.EQUAL,
        participants=["Alice", "Bob", "Charlie"],
    )

    # Net sum of all balances in the system MUST strictly equal zero!
    net_sum = sum(ledger.net_balances.values())
    assert net_sum == Decimal("0.00")

    # Alice paid 100, her share is 33.33 -> net is +66.67
    assert ledger.net_balances["Alice"] == Decimal("66.67")
    assert ledger.net_balances["Bob"] == Decimal("-33.33")
    assert ledger.net_balances["Charlie"] == Decimal("-33.34")


def test_splitwise_percentage_split() -> None:
    ledger = SplitwiseLedger()
    ledger.add_expense(
        paid_by="David",
        total_amount=Decimal("200.00"),
        split_type=SplitType.PERCENTAGE,
        splits=[
            Split("David", Decimal("50.00")),
            Split("Emma", Decimal("30.00")),
            Split("Frank", Decimal("20.00")),
        ],
    )

    assert sum(ledger.net_balances.values()) == Decimal("0.00")
    assert ledger.net_balances["David"] == Decimal("100.00")
    assert ledger.net_balances["Emma"] == Decimal("-60.00")
    assert ledger.net_balances["Frank"] == Decimal("-40.00")


def test_debt_simplification_minimizes_transactions() -> None:
    # Classic transitive debt scenario:
    # A owes B $10, and B owes C $10.
    # Unsimplified = 2 transactions.
    # Simplified = 1 transaction: A pays C $10 directly!
    ledger = SplitwiseLedger()
    # B pays $10 for A
    ledger.add_expense(
        paid_by="Bob",
        total_amount=Decimal("10.00"),
        split_type=SplitType.EXACT,
        splits=[Split("Alice", Decimal("10.00"))],
    )
    # C pays $10 for B
    ledger.add_expense(
        paid_by="Charlie",
        total_amount=Decimal("10.00"),
        split_type=SplitType.EXACT,
        splits=[Split("Bob", Decimal("10.00"))],
    )

    # Bob's net balance should be 0.00 (+10 from A, -10 to C)
    assert ledger.net_balances["Bob"] == Decimal("0.00")

    transactions = ledger.simplify_debts()
    assert len(transactions) == 1
    assert transactions[0].debtor == "Alice"
    assert transactions[0].creditor == "Charlie"
    assert transactions[0].amount == Decimal("10.00")


def test_token_bucket_burst_and_refill() -> None:
    # 5 tokens capacity, 2 tokens per second refill
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)

    # First 5 requests should pass immediately (burst allowed)
    for _ in range(5):
        assert limiter.allow_request() is True

    # 6th request immediately after should be rejected
    assert limiter.allow_request() is False

    # Sleep 0.6s -> should refill at least 1 token (0.6 * 2 = 1.2 tokens)
    time.sleep(0.6)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is False


def test_token_bucket_concurrent_threads() -> None:
    import concurrent.futures

    limiter = TokenBucketRateLimiter(capacity=20, refill_rate=0.0)

    # Launch 50 concurrent threads requesting tokens simultaneously
    def try_request() -> bool:
        return limiter.allow_request()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: try_request(), range(50)))

    # Exactly 20 requests must succeed, and exactly 30 must fail
    assert results.count(True) == 20
    assert results.count(False) == 30
