"""Beginner playground for Module 01 - ACID and the Relational Model.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import sqlite3

# ----------------------------- 1. What the four ACID letters actually promise
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE account (name TEXT PRIMARY KEY, cents INTEGER NOT NULL)")
db.executemany("INSERT INTO account VALUES (?, ?)", [("alice", 10_000), ("bob", 5_000)])
db.commit()


def total_cents():
    return db.execute("SELECT SUM(cents) FROM account").fetchone()[0]


def transfer(amount, crash_midway):
    db.execute("UPDATE account SET cents = cents - ? WHERE name = 'alice'", (amount,))
    if crash_midway:
        raise RuntimeError("power cut between the two updates")
    db.execute("UPDATE account SET cents = cents + ? WHERE name = 'bob'", (amount,))


before = total_cents()
print("money in the bank before:", before)


# ----------------------------------------------------- 2. Crash it on purpose
try:
    transfer(3_000, crash_midway=True)
except RuntimeError as exc:
    print("something went wrong:", exc)
    db.rollback()

after_crash = total_cents()
print("money in the bank after the crash:", after_crash)
assert after_crash == before, "atomicity is broken - money appeared or vanished"
print("Nothing was lost. The half-finished update was thrown away.")


# ------------------------------------------------------- 3. Now let it finish
transfer(3_000, crash_midway=False)
db.commit()

alice = db.execute("SELECT cents FROM account WHERE name = 'alice'").fetchone()[0]
bob = db.execute("SELECT cents FROM account WHERE name = 'bob'").fetchone()[0]
print(f"alice: {alice} cents, bob: {bob} cents")
assert (alice, bob) == (7_000, 8_000)
assert total_cents() == before, "a transfer must never change the bank total"


# --------------------------------- 4. Why tables, and not one big spreadsheet
orders = [
    {"id": 1, "customer": "alice", "city": "Dublin"},
    {"id": 2, "customer": "alice", "city": "Dublin"},
    {"id": 3, "customer": "alice", "city": "Cork"},
]
cities_on_file = {o["city"] for o in orders}
print("cities recorded for ONE customer:", cities_on_file)
assert len(cities_on_file) == 2, "duplication let two versions of the truth coexist"
print("Which is right? Nothing in the data can say. That is the bug.")


print()
print("All checks passed.")
