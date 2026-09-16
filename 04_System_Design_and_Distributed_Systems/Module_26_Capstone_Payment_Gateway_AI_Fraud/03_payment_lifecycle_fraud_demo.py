"""Module 26: Standalone Interactive Demo - Master Capstone Payment Gateway & AI Fraud."""

from project_solution.payment_gateway_platform import (
    FraudEvaluationContext,
    PaymentGatewayPlatform,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 26: MASTER CAPSTONE -- PAYMENT GATEWAY WITH REAL-TIME AI FRAUD")
    print("=" * 80)

    gateway = PaymentGatewayPlatform(fee_percentage=0.029, fixed_fee_cents=30)

    # ---------------------------------------------------------
    # Scenario 1: Legitimate User Payment & Double-Entry Ledger
    # ---------------------------------------------------------
    print("\n--- 1. Legitimate Transaction Processing & Double-Entry Ledger ---")
    legit_context = FraudEvaluationContext(
        amount_cents=10000,           # $100.00
        user_avg_cents=9000,          # Typical $90.00 spend
        user_std_cents=2000,
        hourly_tx_count=1,            # 1 tx in the last hour
        distance_from_billing_km=15,  # 15km from home
    )

    idempotency_key_1 = "idem_key_order_1001"
    res1 = gateway.process_payment(
        idempotency_key=idempotency_key_1,
        customer_id="cust_alice",
        merchant_id="merch_nike",
        amount_cents=10000,
        fraud_ctx=legit_context,
    )

    print(f" Authorization Result:   {res1['status']}")
    print(f" Transaction ID:         {res1['tx_id']}")
    print(f" Gross Amount:           ${res1['amount_cents'] / 100:.2f}")
    print(f" Merchant Payout:        ${res1['merchant_net_cents'] / 100:.2f}")
    print(f" Platform Fee Collected: ${res1['fee_cents'] / 100:.2f}")
    print(f" Idempotent Replay:      {res1['is_idempotent_replay']}")

    # Inspect Ledger Postings
    tx_record = gateway.ledger.transactions[0]
    print("\n Immutable Double-Entry Ledger Entries:")
    for p in tx_record.postings:
        print(f"   - Account: {p.account_id:<22} | Type: {p.entry_type.value:<6} | Amount: ${p.amount_cents / 100:.2f}")
    print(f" Ledger Integrity Audit Passed: {gateway.ledger.verify_ledger_integrity()}")

    # ---------------------------------------------------------
    # Scenario 2: Network Retry & Distributed Idempotency Layer
    # ---------------------------------------------------------
    print("\n--- 2. Network Timeout & Idempotent Retry Protection ---")
    print(" Upstream client timed out waiting for ACK. Retrying identical request...")
    res1_retry = gateway.process_payment(
        idempotency_key=idempotency_key_1,
        customer_id="cust_alice",
        merchant_id="merch_nike",
        amount_cents=10000,
        fraud_ctx=legit_context,
    )

    print(f" Retry Response Status:  {res1_retry['status']}")
    print(f" Matching Tx ID:         {res1_retry['tx_id'] == res1['tx_id']}")
    print(f" Idempotent Replay Flag: {res1_retry['is_idempotent_replay']}")
    print(f" Total Ledger Records:   {len(gateway.ledger.transactions)} (Customer was NOT charged twice!)")

    # ---------------------------------------------------------
    # Scenario 3: Real-Time AI Fraud Detection (Card Stolen Simulation)
    # ---------------------------------------------------------
    print("\n--- 3. Real-Time AI Fraud Detection: High-Risk Anomalous Spike ---")
    fraud_context = FraudEvaluationContext(
        amount_cents=450000,           # $4,500.00 (Huge spike vs normal $50.00)
        user_avg_cents=5000,
        user_std_cents=1500,
        hourly_tx_count=9,             # 9 rapid transactions in the past hour!
        distance_from_billing_km=9500, # 9,500 km away (overseas IP address)
    )

    res_fraud = gateway.process_payment(
        idempotency_key="idem_key_fraud_999",
        customer_id="cust_bob",
        merchant_id="merch_luxury_jewelry",
        amount_cents=450000,
        fraud_ctx=fraud_context,
    )

    print(f" Authorization Result:   {res_fraud['status']}")
    print(f" Decline Reason:         {res_fraud.get('reason')}")
    print(f" ML Fraud Risk Score:    {res_fraud.get('fraud_score')} / 100.0")
    print(f" Policy Decision:        {res_fraud.get('decision')}")
    print(f" Ledger Transactions:    {len(gateway.ledger.transactions)} (No fraudulent money moved!)")
    print(f" Universal Ledger Audit: {gateway.ledger.verify_ledger_integrity()}")

    print("=" * 80)


if __name__ == "__main__":
    main()
