"""Module 26: Master Enterprise Capstone  Payment Gateway Platform with AI Fraud Detection.

Reference implementation of immutable Double-Entry Financial Ledger, distributed
idempotency token deduplication, and real-time AI ML fraud scoring.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import enum
import math
import time
import uuid
from dataclasses import dataclass
from typing import Any

# ============================================================================
# 1. Immutable Double-Entry Financial Ledger
# ============================================================================

class EntryType(enum.StrEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class AccountingDiscrepancyException(Exception):
    """Raised when an accounting transaction violates sum(debits) == sum(credits)."""
    pass


@dataclass(frozen=True)
class LedgerPosting:
    """A single atomic leg of a double-entry financial posting."""
    account_id: str
    entry_type: EntryType
    amount_cents: int

    def __post_init__(self) -> None:
        if self.amount_cents <= 0:
            raise ValueError(f"Posting amount must be strictly positive: {self.amount_cents}")


@dataclass
class FinancialTransactionRecord:
    tx_id: str
    postings: list[LedgerPosting]
    timestamp: float
    description: str


class DoubleEntryLedger:
    """Immutable ledger strictly enforcing sum(debits) == sum(credits) on every transaction."""

    def __init__(self) -> None:
        # account_id -> balance_in_cents (asset accounts normal debit, liability normal credit)
        self.accounts: dict[str, int] = {}
        self.transactions: list[FinancialTransactionRecord] = []

    def get_balance(self, account_id: str) -> int:
        return self.accounts.get(account_id, 0)

    def record_transaction(
        self,
        tx_id: str,
        postings: list[LedgerPosting],
        description: str = "",
    ) -> FinancialTransactionRecord:
        """Atomically validates and commits balanced double-entry postings."""
        total_debits = sum(p.amount_cents for p in postings if p.entry_type == EntryType.DEBIT)
        total_credits = sum(p.amount_cents for p in postings if p.entry_type == EntryType.CREDIT)

        if total_debits != total_credits:
            raise AccountingDiscrepancyException(
                f"Accounting invariant violated! Total debits ({total_debits}c) != total credits ({total_credits}c)"
            )

        # Apply postings to account balances
        for p in postings:
            current = self.accounts.get(p.account_id, 0)
            if p.entry_type == EntryType.DEBIT:
                self.accounts[p.account_id] = current + p.amount_cents
            else:
                self.accounts[p.account_id] = current - p.amount_cents

        record = FinancialTransactionRecord(
            tx_id=tx_id,
            postings=postings,
            timestamp=time.time(),
            description=description,
        )
        self.transactions.append(record)
        return record

    def verify_ledger_integrity(self) -> bool:
        """Audits every historical transaction to confirm mathematical conservation."""
        for tx in self.transactions:
            debits = sum(p.amount_cents for p in tx.postings if p.entry_type == EntryType.DEBIT)
            credits = sum(p.amount_cents for p in tx.postings if p.entry_type == EntryType.CREDIT)
            if debits != credits:
                return False
        return True


# ============================================================================
# 2. Real-Time AI Fraud Detection Engine
# ============================================================================

class FraudDecision(enum.StrEnum):
    APPROVE = "APPROVE"
    CHALLENGE_3DS = "CHALLENGE_3DS"
    DECLINE_FRAUD = "DECLINE_FRAUD"


@dataclass
class FraudEvaluationContext:
    amount_cents: int
    user_avg_cents: float
    user_std_cents: float
    hourly_tx_count: int
    distance_from_billing_km: float


class AIFraudScorer:
    """Computes real-time ML risk scores using behavioral velocity and anomaly signals."""

    @staticmethod
    def score_transaction(ctx: FraudEvaluationContext) -> tuple[float, FraudDecision]:
        """Returns risk score in [0.0, 100.0] and the resulting access control decision."""
        # 1. Transaction Amount Z-Score Feature
        if ctx.user_std_cents > 0:
            z_score = max(0.0, (ctx.amount_cents - ctx.user_avg_cents) / ctx.user_std_cents)
        else:
            z_score = 0.0

        # 2. Velocity Risk Feature: Rapid transactions in 1 hour
        velocity_penalty = max(0, ctx.hourly_tx_count - 2) * 15.0

        # 3. Geolocation Distance Feature: Distance from cardholder's home address
        geo_penalty = min(30.0, (ctx.distance_from_billing_km / 100.0) * 3.0)

        # Sigmoid aggregation
        raw_signal = (z_score * 8.0) + velocity_penalty + geo_penalty
        score = 100.0 / (1.0 + math.exp(-0.08 * (raw_signal - 30.0)))
        score = max(0.0, min(100.0, score))

        # Policy thresholds
        if score >= 75.0:
            decision = FraudDecision.DECLINE_FRAUD
        elif score >= 45.0:
            decision = FraudDecision.CHALLENGE_3DS
        else:
            decision = FraudDecision.APPROVE

        return score, decision


# ============================================================================
# 3. Payment Gateway Platform & Idempotency Layer
# ============================================================================

@dataclass
class IdempotencyRecord:
    key: str
    response: dict[str, Any]
    created_at: float


class PaymentGatewayPlatform:
    """Enterprise Payment Gateway integrating Idempotency, AI Fraud, and Double-Entry Ledger."""

    def __init__(self, fee_percentage: float = 0.029, fixed_fee_cents: int = 30) -> None:
        self.fee_percentage = fee_percentage
        self.fixed_fee_cents = fixed_fee_cents

        self.ledger = DoubleEntryLedger()
        self.idempotency_store: dict[str, IdempotencyRecord] = {}
        self.outbox: list[dict[str, Any]] = []

    def process_payment(
        self,
        idempotency_key: str,
        customer_id: str,
        merchant_id: str,
        amount_cents: int,
        fraud_ctx: FraudEvaluationContext | None = None,
    ) -> dict[str, Any]:
        """Processes payment authorization with strict idempotency and zero overselling."""
        # 1. Idempotency Check: Return previously computed result for identical key
        if idempotency_key in self.idempotency_store:
            cached = self.idempotency_store[idempotency_key]
            return {**cached.response, "is_idempotent_replay": True}

        # 2. Real-Time AI Fraud Evaluation
        if fraud_ctx is not None:
            score, decision = AIFraudScorer.score_transaction(fraud_ctx)
            if decision == FraudDecision.DECLINE_FRAUD:
                resp = {
                    "status": "DECLINED",
                    "reason": "FRAUD_RISK_EXCEEDED",
                    "fraud_score": round(score, 2),
                    "decision": decision.value,
                }
                self.idempotency_store[idempotency_key] = IdempotencyRecord(
                    key=idempotency_key, response=resp, created_at=time.time()
                )
                return {**resp, "is_idempotent_replay": False}

        # 3. Calculate Platform Fee (e.g. 2.9% + 30 cents)
        fee_cents = round(amount_cents * self.fee_percentage) + self.fixed_fee_cents
        merchant_net_cents = amount_cents - fee_cents

        if merchant_net_cents < 0:
            raise ValueError("Transaction amount too small to cover processing fees")

        # 4. Construct Balanced Double-Entry Postings
        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        postings = [
            # Debit customer asset account (total charge)
            LedgerPosting(account_id=f"acct_cust_{customer_id}", entry_type=EntryType.DEBIT, amount_cents=amount_cents),
            # Credit merchant settlement account (net payout)
            LedgerPosting(account_id=f"acct_merch_{merchant_id}", entry_type=EntryType.CREDIT, amount_cents=merchant_net_cents),
            # Credit platform fee revenue account
            LedgerPosting(account_id="acct_platform_fees", entry_type=EntryType.CREDIT, amount_cents=fee_cents),
        ]

        # 5. Commit to Ledger
        self.ledger.record_transaction(tx_id=tx_id, postings=postings, description="Card Charge")

        # 6. Insert into Transactional Outbox
        outbox_event = {
            "event_id": f"evt_{uuid.uuid4().hex[:8]}",
            "event_type": "PaymentAuthorized",
            "tx_id": tx_id,
            "amount_cents": amount_cents,
            "merchant_net_cents": merchant_net_cents,
            "fee_cents": fee_cents,
        }
        self.outbox.append(outbox_event)

        # 7. Persist Idempotency Record
        resp = {
            "status": "AUTHORIZED",
            "tx_id": tx_id,
            "amount_cents": amount_cents,
            "merchant_net_cents": merchant_net_cents,
            "fee_cents": fee_cents,
        }
        self.idempotency_store[idempotency_key] = IdempotencyRecord(
            key=idempotency_key, response=resp, created_at=time.time()
        )

        return {**resp, "is_idempotent_replay": False}
