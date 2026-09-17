# 🐣 Interactive Foundations Playground: Database Internals & ORM Patterns

> *"An ORM translates between relational tables and object graphs while managing transactions."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import sqlite3
```

---

## 1. In-Memory Relational Transactions

SQLite in-memory databases allow testing schema migrations and queries with zero disk footprint.

```python
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
```

---

## 2. Identity Map Pattern

An Identity Map ensures that each database row is represented by exactly one in-memory object instance.

```python
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
```

---

## 3. Transactional Rollback on Failure

Databases rollback uncommitted mutations when a transaction encounters an error.

```python
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
```

---
