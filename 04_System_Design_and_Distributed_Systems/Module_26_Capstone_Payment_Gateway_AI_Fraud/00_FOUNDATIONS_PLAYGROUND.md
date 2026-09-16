# Beginner Playground - Capstone - Payment Gateway with Fraud Detection

> *"The order number on your receipt. Hand it over twice and you do not get charged twice - the till recognises it and shows you the same receipt again."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Idempotency: the same request twice, charged once

The client generates a key per *intent* and sends it with every attempt. The server
records the key with the result.

The subtlety is what a repeat should return. Not an error - the client is not doing
anything wrong, it is recovering from an ambiguous failure. It should return *the
original result*, so the retry is indistinguishable from a success.

```python
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
```

---

## 2. The payment state machine

A payment moves through a fixed set of states, and most of the rules are about
which moves are forbidden. You cannot capture a payment that was never authorised,
and you cannot refund one that was never captured.

Encode the edges once and the invalid operations become impossible rather than
merely discouraged.

```python
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
```

---

## 3. Fraud scoring, and the trade nobody escapes

A fraud model scores each transaction, and you pick a threshold. Every threshold is
a choice between two kinds of mistake:

- **Too low** - you block honest customers. They do not complain, they leave.
- **Too high** - you approve fraud and pay for it.

There is no threshold that avoids both, which is why fraud teams talk about the
cost of each error rather than about accuracy.

```python
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
```

---

## 4. Reconciliation: assume you will disagree

Your ledger and the processor's ledger will drift - a webhook is lost, a timeout
leaves a charge in an unknown state, a refund is recorded twice.

So a payments system has a job that compares both sides every day and reports
differences. Not a fallback for when something breaks: a scheduled, expected part
of running the system.

```python
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
```

---

## 5. Predict before you run

A customer taps Pay, the network stalls, and the app retries. Without an
idempotency key, how many charges appear on the statement? With one, what
does the second request return - an error, or something more useful?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every payment API - Stripe, Adyen, Checkout - requires an idempotency key on
write operations, for exactly this reason. It is the single most important
interface decision in a payments system.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
