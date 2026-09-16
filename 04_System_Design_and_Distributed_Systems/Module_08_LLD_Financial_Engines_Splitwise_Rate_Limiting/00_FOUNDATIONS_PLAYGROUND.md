# Beginner Playground - Rate Limiting and Financial Engines

> *"A rate limiter is a subway turnstile. It does not care who you are or why you are in a hurry - it lets one person through at a time, and the queue outside is not its problem."*


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

## 1. The turnstile, and why the simple one has a hole

A **fixed window** counter is the obvious design: count requests per minute, reset
at the top of the minute.

The hole is at the boundary. A client that waits until the last moment of one
window and then sends again at the start of the next gets *twice* the limit, in
the space of two seconds, entirely within the rules.

```python
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
```

---

## 2. Token bucket: allow bursts, but only what you saved up

Tokens drip into a bucket at a steady rate, up to a maximum. Each request takes
one. Empty bucket means refused.

This is the design most APIs actually use, because it matches how people behave:
idle for a while, then a burst. You can spend what you accumulated, and no more.

```python
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
```

---

## 3. Sliding window: no boundary to exploit

Keep the timestamps and count how many fall within the last 60 seconds, measured
from *now* rather than from a clock boundary. There is no edge to sit on.

It costs memory - you are storing timestamps rather than one integer - which is the
trade. A sliding window *counter* approximates it by weighting the previous
window, and that approximation is what most production limiters actually ship.

```python
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
```

---

## 4. Splitwise: settling the bill with the fewest transfers

Different engine, same module. Four friends, a messy pile of shared expenses.
Everyone's net balance is what they paid minus their share.

Two facts make the problem tractable: the balances always sum to zero, and you do
not need to reverse each individual debt - you only need to move money from the
people who are negative to the people who are positive.

```python
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
```

---

## 5. Predict before you run

A fixed-window limiter allows 100 requests per minute. A client sends 100 at
11:00:59 and 100 more at 11:01:01. Both windows are within their limit. How
many requests arrived in that one real second?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

The fixed-window boundary burst is the reason production rate limiters use
sliding windows or token buckets. It is also a favourite interview follow-up,
because the naive implementation looks obviously correct.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
