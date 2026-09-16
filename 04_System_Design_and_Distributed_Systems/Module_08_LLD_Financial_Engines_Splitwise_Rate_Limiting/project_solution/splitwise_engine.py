#!/usr/bin/env python3
"""Module 08: Splitwise Expense Sharing Engine & Thread-Safe Rate Limiter.

Implements:
- Expense Sharing with Equal, Exact, and Percentage Splits.
- Debt Minimization Algorithm (Cash Flow Simplification).
- Thread-Safe In-Memory Token Bucket Rate Limiter with monotonic clock.
"""

from __future__ import annotations

import heapq
import threading
import time
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum

# ============================================================================
# 1. Splitwise Expense Sharing Engine
# ============================================================================


class SplitType(StrEnum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"


@dataclass(frozen=True)
class Split:
    user_id: str
    amount: Decimal


@dataclass
class Transaction:
    debtor: str
    creditor: str
    amount: Decimal


class SplitwiseLedger:
    """Manages expenses and computes net balances for all participants."""

    def __init__(self) -> None:
        # net_balances: user_id -> Decimal (positive = owed money, negative = owes money)
        self.net_balances: dict[str, Decimal] = {}

    def _ensure_user(self, user_id: str) -> None:
        if user_id not in self.net_balances:
            self.net_balances[user_id] = Decimal("0.00")

    def add_expense(
        self,
        paid_by: str,
        total_amount: Decimal,
        split_type: SplitType,
        splits: list[Split] | None = None,
        participants: list[str] | None = None,
    ) -> None:
        self._ensure_user(paid_by)
        self.net_balances[paid_by] += total_amount

        calculated_splits: list[Split] = []

        if split_type == SplitType.EQUAL:
            if not participants:
                raise ValueError("Participants list required for EQUAL split")
            n = len(participants)
            base_share = (total_amount / Decimal(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            # Penny rounding adjustment
            allocated = Decimal("0.00")
            for i, p in enumerate(participants):
                if i == n - 1:
                    share = total_amount - allocated
                else:
                    share = base_share
                    allocated += share
                calculated_splits.append(Split(p, share))

        elif split_type == SplitType.EXACT:
            if not splits:
                raise ValueError("Splits required for EXACT split")
            total_split = sum(s.amount for s in splits)
            if total_split != total_amount:
                raise ValueError(f"Exact splits sum {total_split} does not match total amount {total_amount}")
            calculated_splits = splits

        elif split_type == SplitType.PERCENTAGE:
            if not splits:
                raise ValueError("Splits required for PERCENTAGE split")
            total_pct = sum(s.amount for s in splits)
            if total_pct != Decimal("100.00"):
                raise ValueError(f"Percentages must sum to 100%, got: {total_pct}%")
            allocated = Decimal("0.00")
            for i, s in enumerate(splits):
                if i == len(splits) - 1:
                    share = total_amount - allocated
                else:
                    share = (total_amount * (s.amount / Decimal("100.00"))).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                    allocated += share
                calculated_splits.append(Split(s.user_id, share))

        # Apply splits to reduce debtor balances
        for s in calculated_splits:
            self._ensure_user(s.user_id)
            self.net_balances[s.user_id] -= s.amount

    def simplify_debts(self) -> list[Transaction]:
        """Greedy Debt Minimization Algorithm.

        Matches the largest debtor with the largest creditor iteratively,
        reducing an O(N^2) web of bilateral IOUs into a minimal set of transactions.
        """
        # Separate into creditors (positive) and debtors (negative)
        # We use heaps for greedy maximum matching
        debtors: list[tuple[float, str]] = []  # max-heap via negative values
        creditors: list[tuple[float, str]] = []

        for user, balance in self.net_balances.items():
            if balance < Decimal("-0.001"):
                # balance is negative; push abs(balance) as negative to make max-heap
                heapq.heappush(debtors, (float(balance), user))
            elif balance > Decimal("0.001"):
                # balance is positive; push -balance to make max-heap
                heapq.heappush(creditors, (-float(balance), user))

        transactions: list[Transaction] = []

        while debtors and creditors:
            debtor_neg_bal, debtor = heapq.heappop(debtors)
            debt_amount = Decimal(str(-debtor_neg_bal)).quantize(Decimal("0.01"))

            creditor_neg_bal, creditor = heapq.heappop(creditors)
            credit_amount = Decimal(str(-creditor_neg_bal)).quantize(Decimal("0.01"))

            settled_amount = min(debt_amount, credit_amount)
            transactions.append(Transaction(debtor=debtor, creditor=creditor, amount=settled_amount))

            remaining_debt = debt_amount - settled_amount
            remaining_credit = credit_amount - settled_amount

            if remaining_debt > Decimal("0.001"):
                heapq.heappush(debtors, (-float(remaining_debt), debtor))
            if remaining_credit > Decimal("0.001"):
                heapq.heappush(creditors, (-float(remaining_credit), creditor))

        return transactions


# ============================================================================
# 2. Thread-Safe Token Bucket Rate Limiter
# ============================================================================


class TokenBucketRateLimiter:
    """Thread-safe Token Bucket Rate Limiter using monotonic time.

    Tokens refill smoothly at `refill_rate` tokens/sec up to `capacity`.
    """

    def __init__(self, capacity: int, refill_rate: float) -> None:
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill_time = time.monotonic()
        self._lock = threading.Lock()

    def allow_request(self, tokens_needed: int = 1) -> bool:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill_time
            self.last_refill_time = now

            # Smooth fractional refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    @property
    def current_tokens(self) -> float:
        with self._lock:
            return self.tokens
