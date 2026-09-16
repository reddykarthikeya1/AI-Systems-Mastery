# Beginner Playground - Flash Sales and Inventory Reservation

> *"Two people reach for the last concert ticket at the same instant. The question is not who is faster - it is whether the system can hand it to both of them."*


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

## 1. The bug, at full speed

Read, check, write. A thousand requests arrive inside the few milliseconds it
takes to complete the first one, so a thousand requests read the same number.

Nothing about this is a race you can win by being quick. The window exists because
there are three steps where there should be one.

```python
STOCK = 100
BUYERS = 1_000

stock = STOCK
reads = [stock] * BUYERS               # all 1,000 read before any of them wrote
sold = 0
for seen in reads:
    if seen > 0:
        sold += 1
        stock -= 1

print(f"items available: {STOCK}, buyers: {BUYERS}, items sold: {sold}")
print(f"stock now: {stock}")
assert sold == BUYERS, "every buyer believed there was stock"
assert stock == STOCK - BUYERS < 0, "900 people bought something that did not exist"
```

---

## 2. One statement, no window

`UPDATE stock SET count = count - 1 WHERE item = ? AND count > 0` does the check
and the decrement in a single operation the database will not interleave. The
number of rows it reports having changed tells you whether you got one.

This is the fix, and it is one line. Not a lock, not a queue, not more servers.

```python
stock = STOCK
sold = 0
rejected = 0
for _ in range(BUYERS):
    # The condition and the decrement are evaluated together, as one step.
    if stock > 0:
        stock -= 1
        sold += 1
    else:
        rejected += 1

print(f"sold: {sold}, rejected: {rejected}, stock: {stock}")
assert sold == STOCK, "exactly the available stock was sold"
assert stock == 0, "and it never went negative"
assert sold + rejected == BUYERS
```

---

## 3. Reserve, then pay: holding stock without losing it

Real checkout is not instant. The buyer needs a few minutes for payment, and
during that time the item must be neither sold to someone else nor lost forever if
they wander off.

So a reservation has an **expiry**. Stock moves to a held state, and a sweeper
returns anything not paid for in time. Skip the expiry and abandoned baskets
permanently consume your inventory.

```python
available = 10
reservations = {}


def reserve(buyer, now, ttl=300):
    global available
    if available <= 0:
        return "sold out"
    available -= 1
    reservations[buyer] = now + ttl
    return "held for 5 minutes"


def expire(now):
    global available
    lapsed = [b for b, deadline in reservations.items() if deadline <= now]
    for buyer in lapsed:
        del reservations[buyer]
        available += 1
    return lapsed


for i in range(10):
    reserve(f"buyer{i}", now=0)
print("all reserved. available:", available, "->", reserve("buyer10", now=0))
assert available == 0

returned = expire(now=400)
print(f"5 minutes later, {len(returned)} unpaid reservations lapsed")
print("available again:", available)
assert available == 10, "abandoned baskets returned to the pool"
```

---

## 4. Why the answer is a queue, not a bigger database

100,000 people hitting one row is a hotspot no amount of hardware fixes - they
all need the same row, and that row can only be changed one at a time.

The architectural answer is to admit it: put the requests in a queue and process
them in order, at whatever rate the inventory can sustain. Everyone gets a fair,
ordered answer, and the database sees a steady, survivable stream.

The visible version of this is the "you are number 4,312 in the queue" page,
which is not a workaround - it is the design.

```python
ARRIVALS = 100_000
DB_CAPACITY_PER_SECOND = 2_000

flood_seconds = ARRIVALS / DB_CAPACITY_PER_SECOND
print(f"{ARRIVALS:,} requests at once against {DB_CAPACITY_PER_SECOND:,}/s capacity")
print(f"  direct: {ARRIVALS / DB_CAPACITY_PER_SECOND:.0f}x over capacity -> timeouts")
print(f"  queued: drained in {flood_seconds:.0f}s, every request answered")
assert ARRIVALS / DB_CAPACITY_PER_SECOND == 50

queue_position = 4_312
wait = queue_position / DB_CAPACITY_PER_SECOND
print(f"the person at position {queue_position:,} waits {wait:.1f}s "
      f"- and can be TOLD that")
assert wait < flood_seconds
print("A known wait is a product decision. An unknown timeout is an outage.")
```

---

## 5. Predict before you run

1,000 buyers, 100 items. Every request reads the stock, sees it is above
zero, and decrements. How many items get sold? The answer is not 100, and the
reason is not that the code is slow.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Overselling a flash sale is a refund, an apology and a news story. The fix is
not more capacity - a faster database oversells faster. It is making the
decision and the decrement one indivisible operation.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
