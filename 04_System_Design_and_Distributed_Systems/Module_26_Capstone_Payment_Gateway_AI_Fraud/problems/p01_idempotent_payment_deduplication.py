"""Problem 01 — Idempotent Payment Deduplication

Topic: 26 Capstone Payment Gateway AI Fraud
Target: Production-grade implementation

Idempotently execute payment transaction checking against idempotency lock store.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def idempotent_payment_deduplication(store: dict[str, dict], idempotency_key: str, payment_payload: dict) -> tuple[dict, bool]:
    """store maps idempotency_key -> {'status': 'SUCCESS', 'result': dict}.
    If idempotency_key exists in store:
        Return (store[idempotency_key]['result'], True)   # cached duplicate replay
    Else:
        Process payment:
        result = {'txn_id': f"txn_{idempotency_key}", 'amount': payment_payload['amount'], 'status': 'PAID'}
        store[idempotency_key] = {'status': 'SUCCESS', 'result': result}
        Return (result, False)                            # freshly processed
    """
    raise NotImplementedError("Implement idempotent_payment_deduplication")
