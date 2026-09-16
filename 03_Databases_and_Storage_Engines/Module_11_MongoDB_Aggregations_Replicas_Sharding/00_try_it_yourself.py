"""Beginner playground for Module 11 - MongoDB - Aggregation, Replica Sets and Sharding.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# ------------------------------------------------------- 1. The conveyor belt
docs = [
    {"region": "north", "amount": 100, "status": "paid"},
    {"region": "north", "amount": 300, "status": "refunded"},
    {"region": "south", "amount": 500, "status": "paid"},
    {"region": "south", "amount": 400, "status": "paid"},
    {"region": "east", "amount": 50, "status": "paid"},
]

examined = {"count": 0}


def stage_match(stream, **conditions):
    for doc in stream:
        examined["count"] += 1
        if all(doc[k] == v for k, v in conditions.items()):
            yield doc


def stage_group(stream, by, field):
    totals = {}
    for doc in stream:
        totals[doc[by]] = totals.get(doc[by], 0) + doc[field]
    yield from ({by: k, "total": v} for k, v in totals.items())


paid_by_region = list(stage_group(stage_match(docs, status="paid"), "region", "amount"))
print("paid revenue by region:", paid_by_region)
assert {d["region"]: d["total"] for d in paid_by_region} == {
    "north": 100, "south": 900, "east": 50
}


# ------------------------------ 2. Stage order is the whole performance story
big = [{"region": "north" if i % 100 else "south", "amount": i} for i in range(10_000)]
sort_work = {"docs": 0}


def sort_stage(stream):
    items = list(stream)
    sort_work["docs"] += len(items)       # what the SORT actually has to handle
    return sorted(items, key=lambda d: d["amount"])


sort_work["docs"] = 0
list(stage_match(sort_stage(big), region="south"))
match_last = sort_work["docs"]

sort_work["docs"] = 0
sort_stage(stage_match(big, region="south"))
match_first = sort_work["docs"]

print(f"documents reaching the $sort stage, $match LAST : {match_last}")
print(f"documents reaching the $sort stage, $match FIRST: {match_first}")
assert match_first < match_last / 5, "filtering early is not a micro-optimisation"


# --------------------------------------- 3. Replica sets: majority or nothing
def can_elect_primary(total_members, reachable):
    return reachable > total_members / 2


print("3-member set, 2 reachable:", can_elect_primary(3, 2))
print("3-member set, 1 reachable:", can_elect_primary(3, 1))
print("2-member set, 1 reachable:", can_elect_primary(2, 1))
assert can_elect_primary(3, 2), "a majority of 3 is 2"
assert not can_elect_primary(3, 1), "a minority must refuse to serve writes"
assert not can_elect_primary(2, 1), "which is why 2 members buys you nothing"
print("Two sides of a split can never BOTH hold a majority. No split brain.")


# ---------------------------------- 4. Sharding: the key you cannot take back
def range_shard(order_id, per_shard=1_000, shards=4):
    return min(order_id // per_shard, shards - 1)


def hash_shard(order_id, shards=4):
    digest = hashlib.md5(str(order_id).encode()).hexdigest()
    return int(digest, 16) % shards


new_orders = range(3_000, 4_000)
by_range = {}
by_hash = {}
for oid in new_orders:
    by_range[range_shard(oid)] = by_range.get(range_shard(oid), 0) + 1
    by_hash[hash_shard(oid)] = by_hash.get(hash_shard(oid), 0) + 1

print("1,000 new orders, range-sharded on a rising id:", dict(sorted(by_range.items())))
print("1,000 new orders, hash-sharded on the same id:", dict(sorted(by_hash.items())))
assert max(by_range.values()) == 1_000, "every single write hit one shard"
assert max(by_hash.values()) < 350, "hashing spreads them out"
print("Four machines. In the first case, three of them are idle.")


print()
print("All checks passed.")
