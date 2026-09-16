"""Beginner playground for Module 04 - PostgreSQL Core and Advanced Types.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json
import sqlite3

# ----------- 1. A type is a promise, and a constraint is a promise with teeth
shop = sqlite3.connect(":memory:")
shop.execute("PRAGMA foreign_keys = ON")
shop.execute('''
    CREATE TABLE product (
        id     INTEGER PRIMARY KEY,
        name   TEXT    NOT NULL,
        cents  INTEGER NOT NULL CHECK (cents > 0),
        status TEXT    NOT NULL CHECK (status IN ('draft', 'live', 'retired'))
    )
''')
shop.execute("INSERT INTO product VALUES (1, 'mug', 1200, 'live')")
shop.commit()
print("one good row inserted")


# ------------------------------------------------ 2. Watch it refuse bad data
def rejected(sql):
    try:
        shop.execute(sql)
    except sqlite3.IntegrityError as exc:
        print("  refused:", exc)
        return True
    return False


assert rejected("INSERT INTO product VALUES (2, 'hat', -500, 'live')"), "negative price"
assert rejected("INSERT INTO product VALUES (3, 'pen', 300, 'pubished')"), "typo status"
assert rejected("INSERT INTO product VALUES (4, NULL, 300, 'live')"), "missing name"

count = shop.execute("SELECT COUNT(*) FROM product").fetchone()[0]
print("rows in the table:", count)
assert count == 1, "none of the three bad writes got through"


# ----------------------------------------------- 3. Foreign keys stop orphans
shop.execute('''
    CREATE TABLE order_line (
        id         INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL REFERENCES product(id),
        quantity   INTEGER NOT NULL CHECK (quantity > 0)
    )
''')
shop.execute("INSERT INTO order_line VALUES (1, 1, 2)")
assert rejected("INSERT INTO order_line VALUES (2, 999, 1)"), "product 999 does not exist"

deleted = rejected("DELETE FROM product WHERE id = 1")
print("deleting a product that still has orders was refused:", deleted)
assert deleted, "the key protects the child rows too, not just the insert"


# ------------------------------------- 4. JSON: flexibility you pay for later
shop.execute("CREATE TABLE event (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)")
shop.execute("INSERT INTO event VALUES (1, ?)", (json.dumps({"prcie": 20}),))
shop.commit()

stored = json.loads(shop.execute("SELECT payload FROM event WHERE id = 1").fetchone()[0])
print("stored happily, typo and all:", stored)
assert "prcie" in stored and "price" not in stored

price = stored.get("price")
print("reading the field you MEANT to store gives:", price)
assert price is None, "the typo becomes a None at read time, far from the write"
print("Rule of thumb: columns for what you query and validate, JSON for the rest.")


print()
print("All checks passed.")
