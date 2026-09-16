"""Beginner playground for Module 18 - Dimensional Modelling and Analytics Pipelines.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from datetime import date

# ---------------------------------------------------- 1. Facts and dimensions
customer_dim = {
    1: {"name": "alice", "state": "Ohio"},
}
sales_fact = [
    {"day": date(2024, 3, 1), "customer_key": 1, "amount": 130},
    {"day": date(2025, 2, 1), "customer_key": 1, "amount": 200},
]


def revenue_by_state():
    totals = {}
    for row in sales_fact:
        state = customer_dim[row["customer_key"]]["state"]
        totals[state] = totals.get(state, 0) + row["amount"]
    return totals


print("revenue by state:", revenue_by_state())
assert revenue_by_state() == {"Ohio": 330}


# ------------------------------- 2. The customer moves, and history teleports
customer_dim[1]["state"] = "Texas"
print("revenue by state after the address update:", revenue_by_state())
assert revenue_by_state() == {"Texas": 330}, "the 2024 Ohio sale moved to Texas"
print("A sale that happened in Ohio is now counted in Texas. History was rewritten.")


# -------------------------- 3. Type 2: keep both versions, stamped with dates
END_OF_TIME = date(9999, 12, 31)
customer_scd2 = [
    {"key": 100, "id": 1, "name": "alice", "state": "Ohio",
     "valid_from": date(2020, 1, 1), "valid_to": date(2024, 6, 30)},
    {"key": 101, "id": 1, "name": "alice", "state": "Texas",
     "valid_from": date(2024, 7, 1), "valid_to": END_OF_TIME},
]


def key_as_of(customer_id, when):
    for version in customer_scd2:
        if version["id"] == customer_id and version["valid_from"] <= when <= version["valid_to"]:
            return version["key"]
    return None


scd2_fact = [
    {"day": r["day"], "customer_key": key_as_of(r["customer_key"], r["day"]),
     "amount": r["amount"]}
    for r in sales_fact
]
by_key = {v["key"]: v for v in customer_scd2}
totals = {}
for row in scd2_fact:
    state = by_key[row["customer_key"]]["state"]
    totals[state] = totals.get(state, 0) + row["amount"]

print("facts now point at:", [r["customer_key"] for r in scd2_fact])
print("revenue by state:", totals)
assert totals == {"Ohio": 130, "Texas": 200}, "each sale counted where it happened"
print("Alice moved. Last year's report did not.")


# ------------------------- 4. Grain: the question to ask before anything else
mixed = [
    {"grain": "order_line", "order": 1, "amount": 60},
    {"grain": "order_line", "order": 1, "amount": 40},
    {"grain": "order", "order": 1, "amount": 100},   # the same money, again
]
print("naive SUM over a mixed-grain table:", sum(r["amount"] for r in mixed))
assert sum(r["amount"] for r in mixed) == 200, "order 1 was worth 100, not 200"

clean = [r for r in mixed if r["grain"] == "order_line"]
print("SUM at one consistent grain:      ", sum(r["amount"] for r in clean))
assert sum(r["amount"] for r in clean) == 100
print("Revenue was overstated by 100%. Nothing crashed. Nothing was logged.")


print()
print("All checks passed.")
