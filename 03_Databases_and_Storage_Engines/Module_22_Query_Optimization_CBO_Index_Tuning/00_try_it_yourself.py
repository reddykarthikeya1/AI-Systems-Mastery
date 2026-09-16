"""Beginner playground for Module 22 - Query Optimization and the Cost-Based Optimizer.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------ 1. The optimizer picks between plans, not between answers
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


# ------------------------------------------------- 2. Filter early, join less
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


# ------------------------------------- 3. Stale statistics: confidently wrong
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


# --------------------------- 4. How to read a plan without knowing everything
plan_node = {"operation": "Seq Scan", "table": "orders",
             "estimated_rows": 100, "actual_rows": 1_000_000}

ratio = plan_node["actual_rows"] / plan_node["estimated_rows"]
print(f"{plan_node['operation']} on {plan_node['table']}: "
      f"estimated {plan_node['estimated_rows']:,}, actual {plan_node['actual_rows']:,}")
print(f"estimate was off by {ratio:,.0f}x")
assert ratio > 100, "this is the signal: run ANALYZE before tuning anything else"


print()
print("All checks passed.")
