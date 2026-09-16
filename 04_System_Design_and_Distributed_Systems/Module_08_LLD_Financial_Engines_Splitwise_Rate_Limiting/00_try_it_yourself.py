"""Beginner playground for Module 08 - Rate Limiting and Financial Engines.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------ 1. The turnstile, and why the simple one has a hole
LIMIT = 100


class FixedWindow:
    def __init__(self):
        self.counts = {}

    def allow(self, minute):
        self.counts[minute] = self.counts.get(minute, 0) + 1
        return self.counts[minute] <= LIMIT


limiter = FixedWindow()
allowed_at_1100 = sum(limiter.allow(minute=1100) for _ in range(LIMIT))
allowed_at_1101 = sum(limiter.allow(minute=1101) for _ in range(LIMIT))

print(f"allowed at 11:00:59 -> {allowed_at_1100}")
print(f"allowed at 11:01:01 -> {allowed_at_1101}")
print(f"in one real second  -> {allowed_at_1100 + allowed_at_1101}")
assert allowed_at_1100 + allowed_at_1101 == 200, "double the limit, within the rules"


# ------------------ 2. Token bucket: allow bursts, but only what you saved up
class TokenBucket:
    def __init__(self, capacity, refill_per_second):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_per_second = refill_per_second

    def advance(self, seconds):
        self.tokens = min(self.capacity, self.tokens + seconds * self.refill_per_second)

    def allow(self):
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


bucket = TokenBucket(capacity=10, refill_per_second=1)
burst = sum(bucket.allow() for _ in range(15))
print(f"15 requests against a full bucket of 10 -> {burst} allowed")
assert burst == 10, "the saved-up burst is spent, then it stops"

bucket.advance(seconds=5)
after_waiting = sum(bucket.allow() for _ in range(15))
print(f"after waiting 5 seconds -> {after_waiting} more allowed")
assert after_waiting == 5, "five seconds of drip, five more requests"


# ---------------------------------- 3. Sliding window: no boundary to exploit
class SlidingWindow:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window = window_seconds
        self.hits = []

    def allow(self, now):
        self.hits = [t for t in self.hits if now - t < self.window]
        if len(self.hits) < self.limit:
            self.hits.append(now)
            return True
        return False


sliding = SlidingWindow(limit=LIMIT, window_seconds=60)
at_end_of_window = sum(sliding.allow(now=59.0) for _ in range(LIMIT))
just_after = sum(sliding.allow(now=61.0) for _ in range(LIMIT))

print(f"allowed at t=59: {at_end_of_window}")
print(f"allowed at t=61: {just_after}")
assert at_end_of_window == LIMIT
assert just_after < LIMIT, "t=59 requests are still inside the 60-second window"
print("No boundary burst, because there is no boundary.")


# ------------------ 4. Splitwise: settling the bill with the fewest transfers
expenses = [
    {"payer": "ana", "amount": 120, "between": ["ana", "bo", "cy", "di"]},
    {"payer": "bo", "amount": 40, "between": ["ana", "bo"]},
    {"payer": "cy", "amount": 80, "between": ["cy", "di"]},
]

balances = dict.fromkeys(["ana", "bo", "cy", "di"], 0.0)
for expense in expenses:
    share = expense["amount"] / len(expense["between"])
    balances[expense["payer"]] += expense["amount"]
    for person in expense["between"]:
        balances[person] -= share

print("net balances:", {k: round(v, 2) for k, v in balances.items()})
assert abs(sum(balances.values())) < 1e-9, "every balance sheet sums to zero"


def settle(balances):
    owed = sorted((v, k) for k, v in balances.items() if v > 1e-9)
    owing = sorted((v, k) for k, v in balances.items() if v < -1e-9)
    transfers = []
    while owed and owing:
        credit, creditor = owed.pop()
        debt, debtor = owing.pop(0)
        amount = min(credit, -debt)
        transfers.append((debtor, creditor, round(amount, 2)))
        if credit - amount > 1e-9:
            owed.append((credit - amount, creditor))
            owed.sort()
        if -debt - amount > 1e-9:
            owing.insert(0, (debt + amount, debtor))
    return transfers


payments = settle(balances)
for debtor, creditor, amount in payments:
    print(f"  {debtor} pays {creditor} {amount}")
assert len(payments) <= len(balances) - 1, "n people never need more than n-1 transfers"
print(f"{len(expenses)} shared expenses settled in {len(payments)} payments.")


print()
print("All checks passed.")
