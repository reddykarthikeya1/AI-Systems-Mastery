"""Beginner playground for Module 26 - Capstone - Payment Gateway with Fraud Detection.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ----------------------- 1. Idempotency: the same request twice, charged once
charges = []
idempotency_store = {}


def charge(key, customer, amount):
    if key in idempotency_store:
        return idempotency_store[key], "replayed"
    charge_id = f"ch_{len(charges) + 1}"
    charges.append({"id": charge_id, "customer": customer, "amount": amount})
    idempotency_store[key] = charge_id
    return charge_id, "created"


first = charge("key-abc", "ana", 4_200)
retry = charge("key-abc", "ana", 4_200)
print("first attempt:", first)
print("retry:        ", retry)
assert first[0] == retry[0], "the same charge id comes back"
assert len(charges) == 1, "the customer was charged once"
assert retry[1] == "replayed"


# ----------------------------------------------- 2. The payment state machine
PAYMENT_TRANSITIONS = {
    "created": {"authorised", "failed"},
    "authorised": {"captured", "voided", "expired"},
    "captured": {"refunded", "disputed"},
    "refunded": set(),
    "voided": set(),
    "failed": set(),
    "expired": set(),
    "disputed": {"refunded"},
}


class Payment:
    def __init__(self, charge_id):
        self.id = charge_id
        self.state = "created"

    def to(self, new_state):
        if new_state not in PAYMENT_TRANSITIONS[self.state]:
            raise ValueError(f"{self.id}: cannot go {self.state} -> {new_state}")
        self.state = new_state
        return self.state


payment = Payment(first[0])
print(" ", payment.to("authorised"))
print(" ", payment.to("captured"))
print(" ", payment.to("refunded"))
try:
    payment.to("captured")
except ValueError as exc:
    print("  refused:", exc)
assert payment.state == "refunded"


# ----------------------------- 3. Fraud scoring, and the trade nobody escapes
transactions = [
    {"id": "t1", "amount": 20, "new_device": False, "country_mismatch": False, "fraud": False},
    {"id": "t2", "amount": 4_000, "new_device": True, "country_mismatch": True, "fraud": True},
    {"id": "t3", "amount": 150, "new_device": True, "country_mismatch": False, "fraud": False},
    {"id": "t4", "amount": 9_500, "new_device": True, "country_mismatch": True, "fraud": True},
    {"id": "t5", "amount": 60, "new_device": False, "country_mismatch": True, "fraud": False},
]


def risk_score(txn):
    score = 0
    score += 40 if txn["amount"] > 1_000 else 0
    score += 25 if txn["new_device"] else 0
    score += 25 if txn["country_mismatch"] else 0
    return score


def evaluate(threshold):
    blocked_good = sum(1 for t in transactions
                       if risk_score(t) >= threshold and not t["fraud"])
    missed_fraud = sum(1 for t in transactions
                       if risk_score(t) < threshold and t["fraud"])
    return blocked_good, missed_fraud


print(f"{'threshold':>10} {'good blocked':>14} {'fraud missed':>14}")
for threshold in (20, 50, 80, 100):
    good, missed = evaluate(threshold)
    print(f"{threshold:>10} {good:>14} {missed:>14}")

assert evaluate(20)[0] > evaluate(80)[0], "a strict threshold blocks honest customers"
assert evaluate(100)[1] > evaluate(80)[1], "a loose one lets fraud through"
assert evaluate(80) == (0, 0), "on this data, 80 separates them cleanly"
print("Real data never separates this cleanly. You are choosing which error to make.")


# -------------------------------- 4. Reconciliation: assume you will disagree
our_ledger = {"ch_1": 4_200, "ch_2": 900, "ch_3": 1_500}
processor_ledger = {"ch_1": 4_200, "ch_2": 950, "ch_4": 700}


def reconcile(ours, theirs):
    return {
        "missing_from_processor": sorted(set(ours) - set(theirs)),
        "missing_from_ours": sorted(set(theirs) - set(ours)),
        "amount_mismatch": sorted(k for k in set(ours) & set(theirs)
                                  if ours[k] != theirs[k]),
    }


report = reconcile(our_ledger, processor_ledger)
for label, items in report.items():
    print(f"  {label:<24} {items}")

assert report["missing_from_processor"] == ["ch_3"], "we think we charged; they do not"
assert report["missing_from_ours"] == ["ch_4"], "they charged; we have no record"
assert report["amount_mismatch"] == ["ch_2"], "50 apart - someone is wrong"
print()
print("Three real problems, found by a scheduled job rather than by a customer.")


print()
print("All checks passed.")
