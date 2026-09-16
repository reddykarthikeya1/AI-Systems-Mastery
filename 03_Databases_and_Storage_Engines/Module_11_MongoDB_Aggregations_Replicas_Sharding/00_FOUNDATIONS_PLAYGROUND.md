# Beginner Playground - MongoDB - Aggregation, Replica Sets and Sharding

> *"An aggregation pipeline is a factory conveyor belt. Put the inspection station at the start and you inspect a few items; put it at the end and you inspect everything you built."*


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

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
```

---

## 1. The conveyor belt

A pipeline is a list of stages. Documents flow in at the top, each stage
transforms or filters them, and what falls off the end is your answer.

The common stages, in plain terms:

| Stage | What it does |
| :--- | :--- |
| `$match` | throw away documents you do not want |
| `$group` | collapse many documents into summaries |
| `$sort` | put them in order |
| `$limit` | keep the first N |

```python
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
```

---

## 2. Stage order is the whole performance story

Filtering first means every later stage handles fewer documents. Filtering last
means you sorted, grouped and shuffled data you were always going to discard.

Put `$match` as early as the logic allows. If an index covers the `$match`, the
database does not even read the rest.

```python
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
```

---

## 3. Replica sets: majority or nothing

A replica set is one primary plus secondaries. If the primary disappears, the
survivors hold an election and promote one of themselves.

The rule that prevents disaster is **majority**. A candidate needs more than half
the votes to win. That is why an even number of members is a bad idea and why
three is the practical minimum: a 2-member set that splits in half has no
majority anywhere, so neither side can elect a primary.

```python
def can_elect_primary(total_members, reachable):
    return reachable > total_members / 2


print("3-member set, 2 reachable:", can_elect_primary(3, 2))
print("3-member set, 1 reachable:", can_elect_primary(3, 1))
print("2-member set, 1 reachable:", can_elect_primary(2, 1))
assert can_elect_primary(3, 2), "a majority of 3 is 2"
assert not can_elect_primary(3, 1), "a minority must refuse to serve writes"
assert not can_elect_primary(2, 1), "which is why 2 members buys you nothing"
print("Two sides of a split can never BOTH hold a majority. No split brain.")
```

---

## 4. Sharding: the key you cannot take back

Sharding splits a collection across machines by a **shard key**. Choose it badly
and the cluster is worse than one machine, because you now have the coordination
costs and none of the parallelism.

The classic mistake: a key that always increases - a timestamp, an auto-increment
id. Under range-based sharding every new document has the highest key there is,
so every write goes to whichever shard owns the top of the range.

```python
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
```

---

## 5. Predict before you run

A pipeline has a `$match` that keeps 1% of documents and a `$sort` over the
whole collection. Does it matter which order you write them in? By roughly how
much, on a million documents?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Choosing a shard key is close to irreversible on a large collection, and
choosing a monotonically increasing one is the classic mistake: every new
write lands on the same shard, so you have bought N machines and are using one.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
