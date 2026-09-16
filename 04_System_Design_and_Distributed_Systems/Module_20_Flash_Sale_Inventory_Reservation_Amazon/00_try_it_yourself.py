"""Beginner playground for Module 20 - Flash Sales and Inventory Reservation.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------------- 1. The bug, at full speed
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


# ------------------------------------------------ 2. One statement, no window
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


# ---------------------- 3. Reserve, then pay: holding stock without losing it
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


# ------------------------ 4. Why the answer is a queue, not a bigger database
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


print()
print("All checks passed.")
