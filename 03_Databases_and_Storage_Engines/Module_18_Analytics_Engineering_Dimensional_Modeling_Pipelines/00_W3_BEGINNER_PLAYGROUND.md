# Beginner Playground - Dimensional Modelling and Analytics Pipelines

> *"A fact table is a shoebox of receipts. Dimensions are the catalogues the receipts point at - and the catalogue you must never overwrite, because last year's receipts still point at it."*

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
from datetime import date
```

---

## 1. Facts and dimensions

Split analytics data in two:

- **Facts** - things that happened, with numbers you add up. One row per event,
  never updated. `(date, customer, product, amount)`.
- **Dimensions** - the descriptions facts point at. Who the customer is, what the
  product is called, which region they are in.

Facts are tall and thin and grow forever. Dimensions are short and wide and
change slowly. Almost every warehouse mistake is a confusion between the two.

```python
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
```

---

## 2. The customer moves, and history teleports

Alice moves to Texas. The obvious thing to do is update her row. Watch what
happens to the 2024 sale she made while she still lived in Ohio.

Nothing errored. No data was lost. And last year's report is now wrong - Ohio's
revenue fell by 130 dollars, retroactively, for a sale that genuinely happened
in Ohio.

This is **Slowly Changing Dimension Type 1**: overwrite in place. It is the right
choice only when the old value was a *mistake*, never when it was the truth at
the time.

```python
customer_dim[1]["state"] = "Texas"
print("revenue by state after the address update:", revenue_by_state())
assert revenue_by_state() == {"Texas": 330}, "the 2024 Ohio sale moved to Texas"
print("A sale that happened in Ohio is now counted in Texas. History was rewritten.")
```

---

## 3. Type 2: keep both versions, stamped with dates

Do not overwrite. Close the old row off with an end date and insert a new one.
Each version gets its own **surrogate key**, and a fact points at the version that
was current *on the day it happened*.

Now last year's report stays right forever, because the fact is nailed to the
version of the truth it was recorded against.

```python
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
```

---

## 4. Grain: the question to ask before anything else

The **grain** is what exactly one row of the fact table represents. "One row per
order line." "One row per page view." Decide it first and write it down.

Mix two grains in one table and every sum is wrong - not obviously wrong, just
quietly inflated, because the order-level rows get counted alongside the line-level
rows that already make them up.

```python
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
```

---

## 5. Predict before you run

A customer moves from Ohio to Texas. You update their row. What happens to
last year's sales report - does Ohio's total go down? Should it?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

"The revenue number changed and nobody deployed anything" is a real incident,
and this is the cause. Overwriting a dimension rewrites history retroactively
across every report that ever used it.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
