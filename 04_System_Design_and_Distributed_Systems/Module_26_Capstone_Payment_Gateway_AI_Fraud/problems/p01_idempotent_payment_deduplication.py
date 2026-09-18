"""Problem 01 — Idempotent Payment Deduplication

Topic: 26 Capstone Payment Gateway AI Fraud
Target: Production-grade implementation

Idempotently execute payment transaction checking against idempotency lock store.

Example:
    >>> store = {}
    >>> idempotent_payment_deduplication(store, 'order_xyz_123', {'amount': 99.95})
    ({'txn_id': 'txn_order_xyz_123', 'amount': 99.95, 'status': 'PAID'}, False)
    >>> idempotent_payment_deduplication(store, 'order_xyz_123', {'amount': 99.95})
    ({'txn_id': 'txn_order_xyz_123', 'amount': 99.95, 'status': 'PAID'}, True)

Hints:
    Hint 1: The idempotency_key, not the payment payload, is what decides
        whether this is a fresh charge or a replay -- a retried request
        with the same key must never charge twice.
    Hint 2: Use a single dict-lookup gate: check `idempotency_key` against
        `store` first -- if present, return the cached result immediately
        with a "replay" flag; otherwise build the result, persist it in
        `store` under that key, and return it with a "fresh" flag.
    Hint 3: The two calls with the same idempotency_key must return the
        exact same result payload (the test asserts `r2 == r1`), so the
        result is computed once and reused, never recomputed on the
        second call; `store` must be mutated in place, not replaced,
        since the test reuses the same `store` reference across both
        calls.
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
