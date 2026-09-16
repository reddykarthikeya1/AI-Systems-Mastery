# Beginner Playground - Query Optimization and the Cost-Based Optimizer

> *"The optimizer is satellite navigation. It does not know the traffic - it estimates from the statistics it collected, and a stale estimate sends you down a closed road with total confidence."*


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

## 1. The optimizer picks between plans, not between answers

You write *what* you want. The optimizer decides *how*. For any non-trivial query
there are many plans that all return the identical answer at wildly different
costs.

It chooses by estimating, and it estimates using **statistics**: roughly how many
rows a table holds, how many distinct values a column has, how they are spread.

```python
stats = {
    "orders": {"rows": 1_000_000},
    "customers": {"rows": 1_000},
}


def estimate_join_cost(build_side, probe_side):
    # Hash join: build a table from one input, then stream the other past it.
    # Building is expensive, probing is cheap. So build from the SMALL side.
    return stats[build_side]["rows"] * 10 + stats[probe_side]["rows"]


small_first = estimate_join_cost("customers", "orders")
large_first = estimate_join_cost("orders", "customers")
print(f"build from customers (1k rows): cost {small_first:,}")
print(f"build from orders (1M rows):    cost {large_first:,}")
assert small_first < large_first, "build the hash table from the smaller input"
print("Same rows out. Same answer. One plan costs ~1000x the other.")
```

---

## 2. Filter early, join less

Joining then filtering makes the database build a large intermediate result and
throw most of it away. Filtering first means the join handles a fraction of the
rows.

You usually do not write this transformation yourself - a good optimizer pushes
the predicate down for you. Knowing it happens is what lets you read a plan and
notice when it *has not*.

```python
rows_processed = {"count": 0}
orders = [{"id": i, "customer": i % 1_000, "status": "cancelled" if i % 100 else "paid"}
          for i in range(10_000)]
customers = {i: {"id": i, "name": f"customer{i}"} for i in range(1_000)}


def join_then_filter():
    joined = []
    for order in orders:
        rows_processed["count"] += 1
        joined.append((order, customers[order["customer"]]))
    return [pair for pair in joined if pair[0]["status"] == "paid"]


def filter_then_join():
    result = []
    for order in orders:
        if order["status"] != "paid":
            continue
        rows_processed["count"] += 1
        result.append((order, customers[order["customer"]]))
    return result


rows_processed["count"] = 0
late = join_then_filter()
late_cost = rows_processed["count"]

rows_processed["count"] = 0
early = filter_then_join()
early_cost = rows_processed["count"]

print(f"join then filter: {late_cost:,} rows joined")
print(f"filter then join: {early_cost:,} rows joined")
assert len(late) == len(early), "identical result set"
assert early_cost < late_cost / 50, "the filter removed 99% before the expensive part"
```

---

## 3. Stale statistics: confidently wrong

The optimizer trusts its statistics completely. If they say a table holds 100 rows
and it actually holds a million, it will pick the plan that is right for 100 rows
and execute it against a million.

The answer stays correct. Only the time changes - by orders of magnitude.

```python
stats["orders"]["rows"] = 100          # yesterday's truth, never refreshed
actual_orders = 1_000_000

planned = estimate_join_cost("orders", "customers")
print(f"optimizer's estimate with stale stats: {planned:,}")

stats["orders"]["rows"] = actual_orders
real_cost = estimate_join_cost("orders", "customers")
print(f"what that plan actually costs:         {real_cost:,}")
assert real_cost > planned * 1_000, "off by a factor of ten thousand"
print()
print("Nothing is broken. Nothing is logged. ANALYZE fixes it in seconds -")
print("if you know to look.")
```

---

## 4. How to read a plan without knowing everything

You do not need to understand every operator. Three habits catch most problems:

1. **Look for a scan where you expected a seek.** A full scan on a big table with
   a selective `WHERE` means the index is missing, unusable, or not worth using.
2. **Compare estimated rows with actual rows.** A big gap means the statistics are
   lying, and every decision built on them is suspect.
3. **Find the most expensive node and start there.** The plan is a tree; the time
   is usually concentrated in one or two places.

```python
plan_node = {"operation": "Seq Scan", "table": "orders",
             "estimated_rows": 100, "actual_rows": 1_000_000}

ratio = plan_node["actual_rows"] / plan_node["estimated_rows"]
print(f"{plan_node['operation']} on {plan_node['table']}: "
      f"estimated {plan_node['estimated_rows']:,}, actual {plan_node['actual_rows']:,}")
print(f"estimate was off by {ratio:,.0f}x")
assert ratio > 100, "this is the signal: run ANALYZE before tuning anything else"
```

---

## 5. Predict before you run

A table had 100 rows when statistics were last gathered. It now has a
million. The optimizer plans a join assuming 100. What does it choose, and is
the answer it returns still correct?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

"It was fast yesterday and slow today with no code change" is nearly always
this: the data grew, the statistics did not, and the plan flipped. The fix is
usually one `ANALYZE`, and knowing that saves hours.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
