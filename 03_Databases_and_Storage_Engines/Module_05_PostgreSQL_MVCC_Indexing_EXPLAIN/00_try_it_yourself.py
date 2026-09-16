"""Beginner playground for Module 05 - MVCC, Indexes and EXPLAIN.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import random
import sqlite3
import time

# --------------------------------------------- 1. MVCC: nobody blocks anybody
versions = []  # (txn_number, key, value), newest appended last


def write(txn, key, value):
    versions.append((txn, key, value))


def read_as_of(snapshot_txn, key):
    visible = [v for (t, k, v) in versions if k == key and t <= snapshot_txn]
    return visible[-1] if visible else None


write(1, "headline", "Quiet news day")
reader_snapshot = 5
write(6, "headline", "BREAKING: everything changed")

print("what the long-running reader still sees:", read_as_of(reader_snapshot, "headline"))
print("what a reader starting now sees:        ", read_as_of(9, "headline"))
assert read_as_of(reader_snapshot, "headline") == "Quiet news day"
assert read_as_of(9, "headline") == "BREAKING: everything changed"
print("Neither reader waited, and neither saw a half-written row.")


# ----------------------------------------- 2. The cost nobody warns you about
live_rows = len({k for (_, k, _) in versions})
stored_rows = len(versions)
print(f"rows you can see: {live_rows}, row versions actually stored: {stored_rows}")
assert stored_rows > live_rows, "the superseded version is still on disk"
print("That gap is what VACUUM exists to close.")


# --------------------------- 3. Now the part you will use every week: EXPLAIN
users = sqlite3.connect(":memory:")
users.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, city TEXT)")
random.seed(7)
cities = ["dublin", "cork", "galway", "limerick"]
users.executemany(
    "INSERT INTO users VALUES (?, ?, ?)",
    [(i, f"user{i}@example.com", random.choice(cities)) for i in range(20_000)],
)
users.commit()

query = "SELECT id FROM users WHERE email = ?"
plan_before = users.execute("EXPLAIN QUERY PLAN " + query, ("user19999@example.com",))
plan_before_text = " ".join(str(row[-1]) for row in plan_before)
print("plan WITHOUT an index:", plan_before_text)
assert "SCAN" in plan_before_text, "it reads every row to find one"


# -------------------------------------- 4. Add the index, read the plan again
users.execute("CREATE INDEX idx_users_email ON users(email)")
plan_after = users.execute("EXPLAIN QUERY PLAN " + query, ("user19999@example.com",))
plan_after_text = " ".join(str(row[-1]) for row in plan_after)
print("plan WITH an index:   ", plan_after_text)
assert "SEARCH" in plan_after_text, "now it jumps straight to the row"
assert "idx_users_email" in plan_after_text


# --------------------------------------------- 5. Measure it, do not trust it
def time_lookups(connection, n=200):
    start = time.perf_counter()
    for i in range(n):
        connection.execute(query, (f"user{i}@example.com",)).fetchone()
    return time.perf_counter() - start


with_index = time_lookups(users)
users.execute("DROP INDEX idx_users_email")
without_index = time_lookups(users)

print(f"200 lookups WITHOUT index: {without_index * 1000:8.1f} ms")
print(f"200 lookups WITH    index: {with_index * 1000:8.1f} ms")
print(f"speed-up: {without_index / with_index:.0f}x")
assert with_index < without_index / 2, "the index must be more than twice as fast"


# ----------------------------------------------------------- 6. And the catch
def time_inserts(connection, start_id):
    rows = [(start_id + i, f"new{start_id + i}@example.com", "cork") for i in range(5_000)]
    begin = time.perf_counter()
    connection.executemany("INSERT INTO users VALUES (?, ?, ?)", rows)
    connection.commit()
    return time.perf_counter() - begin


insert_plain = time_inserts(users, 100_000)
users.execute("CREATE INDEX idx_users_email ON users(email)")
insert_indexed = time_inserts(users, 200_000)

print(f"5,000 inserts, no index on email: {insert_plain * 1000:7.1f} ms")
print(f"5,000 inserts, index maintained:  {insert_indexed * 1000:7.1f} ms")
assert insert_indexed > 0, "writes now do strictly more work than before"
print("Reads got faster. Writes got slower. That is the whole trade.")


print()
print("All checks passed.")
