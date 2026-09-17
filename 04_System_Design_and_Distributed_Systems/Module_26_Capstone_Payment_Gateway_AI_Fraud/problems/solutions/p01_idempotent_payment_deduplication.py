"""Reference Solution — Problem 01: Idempotent Payment Deduplication

Topic: 26 Capstone Payment Gateway AI Fraud
"""

from __future__ import annotations


def idempotent_payment_deduplication(store: dict[str, dict], idempotency_key: str, payment_payload: dict) -> tuple[dict, bool]:
    if idempotency_key in store:
        return (store[idempotency_key]['result'], True)
    res = {
        'txn_id': f"txn_{idempotency_key}",
        'amount': payment_payload.get('amount', 0.0),
        'status': 'PAID'
    }
    store[idempotency_key] = {'status': 'SUCCESS', 'result': res}
    return (res, False)
