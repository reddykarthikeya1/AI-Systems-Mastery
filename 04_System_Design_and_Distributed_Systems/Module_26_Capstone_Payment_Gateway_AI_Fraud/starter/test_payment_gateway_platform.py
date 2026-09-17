"""Unit and integration test suite for Module 26: Master Enterprise Capstone."""

import pytest
from payment_gateway_platform import (
    AccountingDiscrepancyException,
    AIFraudScorer,
    DoubleEntryLedger,
    EntryType,
    FraudDecision,
    FraudEvaluationContext,
    LedgerPosting,
    PaymentGatewayPlatform,
)


def test_double_entry_ledger_balanced_postings() -> None:
    ledger = DoubleEntryLedger()
    postings = [
        LedgerPosting("acct_alice", EntryType.DEBIT, 1000),
        LedgerPosting("acct_bob", EntryType.CREDIT, 1000),
    ]
    tx = ledger.record_transaction("tx_1", postings, "Test Transfer")
    assert tx.tx_id == "tx_1"
    assert ledger.get_balance("acct_alice") == 1000
    assert ledger.get_balance("acct_bob") == -1000
    assert ledger.verify_ledger_integrity() is True


def test_double_entry_ledger_unbalanced_discrepancy() -> None:
    ledger = DoubleEntryLedger()
    # Unbalanced: 1000 debit vs 800 credit
    postings = [
        LedgerPosting("acct_alice", EntryType.DEBIT, 1000),
        LedgerPosting("acct_bob", EntryType.CREDIT, 800),
    ]
    with pytest.raises(AccountingDiscrepancyException):
        ledger.record_transaction("tx_unbalanced", postings)


def test_payment_authorization_and_fee_math() -> None:
    gateway = PaymentGatewayPlatform(fee_percentage=0.029, fixed_fee_cents=30)

    # $100.00 transaction -> Fee: 2.9% * 10000 = 290 + 30 = 320c ($3.20)
    # Merchant payout: 10000 - 320 = 9680c ($96.80)
    res = gateway.process_payment(
        idempotency_key="key_001",
        customer_id="alice",
        merchant_id="merchant_x",
        amount_cents=10000,
    )

    assert res["status"] == "AUTHORIZED"
    assert res["amount_cents"] == 10000
    assert res["fee_cents"] == 320
    assert res["merchant_net_cents"] == 9680
    assert res["is_idempotent_replay"] is False
    assert len(gateway.outbox) == 1
    assert gateway.ledger.verify_ledger_integrity() is True


def test_idempotent_replay_protection() -> None:
    gateway = PaymentGatewayPlatform()

    res1 = gateway.process_payment(
        idempotency_key="unique_order_key_42",
        customer_id="alice",
        merchant_id="merchant_y",
        amount_cents=5000,
    )

    # Replay with identical key
    res2 = gateway.process_payment(
        idempotency_key="unique_order_key_42",
        customer_id="alice",
        merchant_id="merchant_y",
        amount_cents=5000,
    )

    assert res2["is_idempotent_replay"] is True
    assert res2["tx_id"] == res1["tx_id"]
    # Only 1 transaction recorded in ledger
    assert len(gateway.ledger.transactions) == 1


def test_ai_fraud_scorer_detection() -> None:
    # Low risk normal transaction
    legit_ctx = FraudEvaluationContext(
        amount_cents=5000,
        user_avg_cents=5000,
        user_std_cents=1000,
        hourly_tx_count=1,
        distance_from_billing_km=5,
    )
    score_legit, decision_legit = AIFraudScorer.score_transaction(legit_ctx)
    assert score_legit < 45.0
    assert decision_legit == FraudDecision.APPROVE

    # Extreme risk anomaly (overseas + velocity burst + 50x amount)
    fraud_ctx = FraudEvaluationContext(
        amount_cents=500000,
        user_avg_cents=10000,
        user_std_cents=2000,
        hourly_tx_count=8,
        distance_from_billing_km=10000,
    )
    score_fraud, decision_fraud = AIFraudScorer.score_transaction(fraud_ctx)
    assert score_fraud >= 75.0
    assert decision_fraud == FraudDecision.DECLINE_FRAUD


def test_gateway_declines_fraud_without_touching_ledger() -> None:
    gateway = PaymentGatewayPlatform()
    fraud_ctx = FraudEvaluationContext(
        amount_cents=900000,
        user_avg_cents=5000,
        user_std_cents=1000,
        hourly_tx_count=10,
        distance_from_billing_km=12000,
    )

    res = gateway.process_payment(
        idempotency_key="fraud_key_test",
        customer_id="attacker",
        merchant_id="merchant_z",
        amount_cents=900000,
        fraud_ctx=fraud_ctx,
    )

    assert res["status"] == "DECLINED"
    assert res["reason"] == "FRAUD_RISK_EXCEEDED"
    assert len(gateway.ledger.transactions) == 0  # No ledger postings committed!
