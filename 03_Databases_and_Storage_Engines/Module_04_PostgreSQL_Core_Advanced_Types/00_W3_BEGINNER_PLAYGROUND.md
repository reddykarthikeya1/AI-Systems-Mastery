# Beginner Playground - PostgreSQL Core and Advanced Types

> *"A column type is a promise the database keeps even when your code forgets to."*

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
import json
import sqlite3
```

---

## 1. A type is a promise, and a constraint is a promise with teeth

Saying a column is an `INTEGER` stops you storing "banana" in it. Saying
`CHECK (cents > 0)` stops you storing -500. The difference matters: the type
catches a *mistake*, the constraint catches a *bug*.

Put the rule in the database and it holds for every writer, forever - your API,
your batch job, the intern with a `psql` prompt at 2am. Put it only in your
application and it holds for exactly one of those.

```python
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
```

---

## 2. Watch it refuse bad data

Three writes that an application-level check would have to remember every single
time. The database remembers for you.

```python
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
```

---

## 3. Foreign keys stop orphans

An order line pointing at a product that does not exist is a row you can never
render, never refund and never explain. A foreign key makes that row impossible
rather than merely unlikely.

```python
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
```

---

## 4. JSON: flexibility you pay for later

PostgreSQL's `jsonb` (and SQLite's JSON support) lets you store a whole object in
one column. That is genuinely useful for data whose shape you do not control -
a webhook payload, a third-party API response.

The cost is that you just gave up the promise. A JSON blob will happily accept a
misspelled key, a price stored as a string, or a field nobody knew existed. The
database cannot object, because you never told it what the shape should be.

```python
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
```

---

## 5. Predict before you run

The JSON section stores `{"prcie": 20}` - a typo. A `CHECK (price > 0)`
constraint would have caught that instantly on a real column. Will the database
catch it inside a JSON blob? What is the first moment anybody finds out?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every "how did a negative price get into production" incident is this module.
The answer is almost always that the rule lived in one application, and a
second application - a migration script, an admin tool, a colleague's
one-off fix - wrote to the table without it.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
