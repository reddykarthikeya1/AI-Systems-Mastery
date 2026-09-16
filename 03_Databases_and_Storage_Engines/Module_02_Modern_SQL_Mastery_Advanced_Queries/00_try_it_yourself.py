"""Beginner playground for Module 02 - Modern SQL - Window Functions and CTEs.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import sqlite3

# ----------------------------------- 1. A table small enough to check by hand
print("SQLite version:", sqlite3.sqlite_version)
assert sqlite3.sqlite_version_info >= (3, 25), "window functions need SQLite 3.25+"

sales_db = sqlite3.connect(":memory:")
sales_db.execute("CREATE TABLE sale (day INTEGER, region TEXT, amount INTEGER)")
sales_db.executemany("INSERT INTO sale VALUES (?, ?, ?)", [
    (1, "north", 100), (2, "north", 300), (3, "north", 200),
    (1, "south", 500), (2, "south", 100), (3, "south", 400),
])
sales_db.commit()


# --------------------------------------------- 2. GROUP BY collapses the rows
grouped = sales_db.execute(
    "SELECT region, SUM(amount) FROM sale GROUP BY region ORDER BY region"
).fetchall()
print("six input rows collapsed to:", grouped)
assert grouped == [("north", 600), ("south", 1000)]
assert len(grouped) == 2, "the per-day detail is gone for good"


# ------------------------------ 3. A window keeps every row and adds a column
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


# -------------------------------------------- 4. A CTE is a named scratch pad
top_days = sales_db.execute(
    "WITH daily AS ("
    "    SELECT day, SUM(amount) AS total FROM sale GROUP BY day"
    "), ranked AS ("
    "    SELECT day, total, RANK() OVER (ORDER BY total DESC) AS place FROM daily"
    ") SELECT day, total, place FROM ranked WHERE place <= 2 ORDER BY day"
).fetchall()

print("busiest days:", top_days)
assert top_days == [(1, 600, 1), (3, 600, 1)], "day 1 and day 3 BOTH total 600"


# ------------------------------- 5. Ties: the bug you only find in production
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


print()
print("All checks passed.")
