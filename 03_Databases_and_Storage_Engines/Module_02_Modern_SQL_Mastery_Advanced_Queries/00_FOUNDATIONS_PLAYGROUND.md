# Beginner Playground - Modern SQL - Window Functions and CTEs

> *"GROUP BY hands you the summary and takes away the receipts. A window function hands you both."*

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
import sqlite3
```

---

## 1. A table small enough to check by hand

Six sales across two regions. Small enough that you can verify every number
yourself - which is exactly the right size to learn on.

```python
print("SQLite version:", sqlite3.sqlite_version)
assert sqlite3.sqlite_version_info >= (3, 25), "window functions need SQLite 3.25+"

sales_db = sqlite3.connect(":memory:")
sales_db.execute("CREATE TABLE sale (day INTEGER, region TEXT, amount INTEGER)")
sales_db.executemany("INSERT INTO sale VALUES (?, ?, ?)", [
    (1, "north", 100), (2, "north", 300), (3, "north", 200),
    (1, "south", 500), (2, "south", 100), (3, "south", 400),
])
sales_db.commit()
```

---

## 2. GROUP BY collapses the rows

`GROUP BY` answers "what is the total per region" by throwing the individual
sales away. That is the right tool when you only want the summary - and the
wrong one the moment somebody asks "which day was that?".

```python
grouped = sales_db.execute(
    "SELECT region, SUM(amount) FROM sale GROUP BY region ORDER BY region"
).fetchall()
print("six input rows collapsed to:", grouped)
assert grouped == [("north", 600), ("south", 1000)]
assert len(grouped) == 2, "the per-day detail is gone for good"
```

---

## 3. A window keeps every row and adds a column

`OVER (PARTITION BY region ORDER BY day)` means: *for each row*, look at the rows
in the same region up to and including this day, and total them.

Six rows in, six rows out - each with a running total beside it.

```python
running = sales_db.execute(
    "SELECT day, region, amount, "
    "       SUM(amount) OVER (PARTITION BY region ORDER BY day) AS running "
    "FROM sale ORDER BY region, day"
).fetchall()

for row in running:
    print(f"  day {row[0]}  {row[1]:<6} sold {row[2]:>4}   running {row[3]:>4}")

assert len(running) == 6, "a window function never collapses rows"
north_running = [r[3] for r in running if r[1] == "north"]
assert north_running == [100, 400, 600], "each row sees itself plus everything before"
```

---

## 4. A CTE is a named scratch pad

`WITH name AS (...)` gives a query a name so the next one can use it. You read it
top to bottom like a recipe, instead of inside-out like nested brackets.

```python
top_days = sales_db.execute(
    "WITH daily AS ("
    "    SELECT day, SUM(amount) AS total FROM sale GROUP BY day"
    "), ranked AS ("
    "    SELECT day, total, RANK() OVER (ORDER BY total DESC) AS place FROM daily"
    ") SELECT day, total, place FROM ranked WHERE place <= 2 ORDER BY day"
).fetchall()

print("busiest days:", top_days)
assert top_days == [(1, 600, 1), (3, 600, 1)], "day 1 and day 3 BOTH total 600"
```

---

## 5. Ties: the bug you only find in production

Look again at what just happened. We asked for "the top 2 days" and got two rows
both ranked **1** - because day 1 (100 + 500) and day 3 (200 + 400) are level on
600. There is no rank 2 at all. `RANK()` leaves a gap after a tie and jumps
straight to 3.

That is not a quirk to memorise, it is a choice you have to make:

| Function | On a two-way tie | Next value | Use it when |
| :--- | :--- | :--- | :--- |
| `RANK()` | `1, 1` | `3` | Olympic medals - two golds, no silver |
| `DENSE_RANK()` | `1, 1` | `2` | "which price tier is this" |
| `ROW_NUMBER()` | `1, 2` | `3` | You need exactly N rows, tie or not |

Pick `ROW_NUMBER()` for "give me 10 rows" and you always get 10. Pick `RANK()`
and a tie at the boundary quietly hands you 11.

```python
ranks = sales_db.execute(
    "WITH daily AS (SELECT day, SUM(amount) AS total FROM sale GROUP BY day) "
    "SELECT day, total, "
    "       RANK()       OVER (ORDER BY total DESC) AS with_gaps, "
    "       DENSE_RANK() OVER (ORDER BY total DESC) AS no_gaps, "
    "       ROW_NUMBER() OVER (ORDER BY total DESC) AS forced "
    "FROM daily ORDER BY total DESC, day"
).fetchall()

for day, total, with_gaps, no_gaps, forced in ranks:
    print(f"  day {day}  total {total:>4}   RANK {with_gaps}   "
          f"DENSE_RANK {no_gaps}   ROW_NUMBER {forced}")

assert [r[2] for r in ranks] == [1, 1, 3], "RANK skips 2 after a two-way tie"
assert [r[3] for r in ranks] == [1, 1, 2], "DENSE_RANK never leaves a gap"
assert [r[4] for r in ranks] == [1, 2, 3], "ROW_NUMBER breaks the tie arbitrarily"
```

---

## 6. Predict before you run

In the running-total query, change `ORDER BY day` to `ORDER BY amount`. The
numbers in the `running` column will change. Will the *last* value in that
column change too? Why or why not?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every "balance after this transaction" column on a bank statement, every "rank
within your region" dashboard, and every "vs. last month" figure is a window
function. Doing it in application code instead means dragging every row across
the network to perform arithmetic the database could have done in place.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
