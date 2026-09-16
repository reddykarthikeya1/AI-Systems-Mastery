"""Beginner playground for Module 13 - Redis Sentinel, Clustering and Lua.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# ------------------------------------------ 1. Why one watchman is not enough
QUORUM = 2


def should_fail_over(reports):
    down_votes = sum(1 for reachable in reports.values() if not reachable)
    return down_votes >= QUORUM


one_bad_cable = {"sentinel1": False, "sentinel2": True, "sentinel3": True}
really_down = {"sentinel1": False, "sentinel2": False, "sentinel3": False}

print("one sentinel cannot see the primary ->", should_fail_over(one_bad_cable))
print("all three cannot see the primary   ->", should_fail_over(really_down))
assert not should_fail_over(one_bad_cable), "one opinion is not evidence"
assert should_fail_over(really_down)


# -------------------------------------------------- 2. The last item in stock
stock = {"tickets": 1}
sold = []


def buy_naive(customer):
    current = stock["tickets"]          # 1. read
    if current > 0:                     # 2. decide
        return ("decided_to_buy", customer, current)
    return ("sold_out", customer, current)


decision_a = buy_naive("alice")
decision_b = buy_naive("bob")           # both read before either wrote

for _, customer, _ in (decision_a, decision_b):
    stock["tickets"] -= 1               # 3. write
    sold.append(customer)

print("tickets sold:", sold, " stock now:", stock["tickets"])
assert len(sold) == 2 and stock["tickets"] == -1, "we sold a ticket that did not exist"
print("Negative stock. Somebody is getting an apology email.")


# -------------------------------------------- 3. Make it one indivisible step
stock = {"tickets": 1}
sold = []


def buy_atomic(customer):
    # Everything inside this function is the Lua script: it runs start to finish
    # with no other client able to see or change `stock` partway through.
    if stock["tickets"] > 0:
        stock["tickets"] -= 1
        sold.append(customer)
        return "bought"
    return "sold out"


print("alice:", buy_atomic("alice"))
print("bob:  ", buy_atomic("bob"))
print("tickets sold:", sold, " stock now:", stock["tickets"])
assert sold == ["alice"], "exactly one ticket existed, exactly one was sold"
assert stock["tickets"] == 0, "stock can never go negative now"


# ----------------------- 4. Cluster mode: 16,384 slots and the multi-key rule
def slot_of(key):
    tag_start = key.find("{")
    tag_end = key.find("}", tag_start + 1)
    if tag_start != -1 and tag_end > tag_start + 1:
        key = key[tag_start + 1:tag_end]
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % 16_384


plain_a, plain_b = slot_of("user:1:cart"), slot_of("user:1:orders")
print(f"user:1:cart -> slot {plain_a},  user:1:orders -> slot {plain_b}")
assert plain_a != plain_b, "similar-looking keys land on different machines"

tagged_a, tagged_b = slot_of("{user:1}:cart"), slot_of("{user:1}:orders")
print(f"{{user:1}}:cart -> slot {tagged_a},  {{user:1}}:orders -> slot {tagged_b}")
assert tagged_a == tagged_b, "the hash tag forces them into the same slot"
print("Same slot means same node, which means multi-key commands are possible.")


print()
print("All checks passed.")
