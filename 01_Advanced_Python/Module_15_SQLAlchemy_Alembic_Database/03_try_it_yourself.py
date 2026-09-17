"""Beginner playground for Module 15 - Database Internals & ORM Patterns.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import sqlite3

# -------------------------------------------- 1. In-Memory Relational Transactions
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
conn.execute("INSERT INTO products VALUES (1, 'Keyboard', 49.99)")
conn.commit()

cursor = conn.cursor()
cursor.execute("SELECT name, price FROM products WHERE id = 1")
row = cursor.fetchone()
assert row == ("Keyboard", 49.99)
assert len(row) == 2
print(f"Queried product row: {row}")

# -------------------------------------------- 2. Identity Map Pattern
class IdentityMap:
    def __init__(self):
        self._cache = {}

    def get_or_set(self, pk, entity):
        if pk not in self._cache:
            self._cache[pk] = entity
        return self._cache[pk]

imap = IdentityMap()
e1 = imap.get_or_set(1, {"id": 1, "name": "Alice"})
e2 = imap.get_or_set(1, {"id": 1, "name": "Different"})
assert e1 is e2
assert e2["name"] == "Alice"
print("Identity map preserved single object reference for PK 1.")

# -------------------------------------------- 3. Transactional Rollback on Failure
try:
    with conn:
        conn.execute("INSERT INTO products VALUES (2, 'Mouse', 19.99)")
        raise RuntimeError("Simulated transaction abort")
except RuntimeError:
    pass

cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
assert count == 1
print(f"Transaction safely rolled back: row count remained {count}")

print()
print("All checks passed.")
