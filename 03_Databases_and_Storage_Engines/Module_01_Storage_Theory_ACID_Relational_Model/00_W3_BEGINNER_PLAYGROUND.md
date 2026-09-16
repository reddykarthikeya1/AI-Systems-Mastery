# Beginner Playground - ACID and the Relational Model

> *"A transaction is a stapler. Either every page of the transfer gets stapled together, or none of them do."*

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

## 1. What the four ACID letters actually promise

Forget the textbook definitions for a minute. You are moving $30 from Alice to
Bob. That is *two* separate writes: take it off Alice, put it on Bob.

- **A**tomic - both writes happen, or neither does. No "$30 in mid-air".
- **C**onsistent - the rules you declared (nobody goes negative) still hold after.
- **I**solated - someone reading the balances never catches you mid-transfer.
- **D**urable - once the database says "done", a power cut cannot undo it.

Only the first one needs a demo to believe. Let us break a transfer on purpose.

```python
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
```

---

## 2. Crash it on purpose

The first `UPDATE` really did run. Alice really was $30 lighter for a moment.
Then we tell the database to forget the whole thing ever happened.

```python
try:
    transfer(3_000, crash_midway=True)
except RuntimeError as exc:
    print("something went wrong:", exc)
    db.rollback()

after_crash = total_cents()
print("money in the bank after the crash:", after_crash)
assert after_crash == before, "atomicity is broken - money appeared or vanished"
print("Nothing was lost. The half-finished update was thrown away.")
```

---

## 3. Now let it finish

Same function, no crash. This time we commit, and the change becomes permanent.

```python
transfer(3_000, crash_midway=False)
db.commit()

alice = db.execute("SELECT cents FROM account WHERE name = 'alice'").fetchone()[0]
bob = db.execute("SELECT cents FROM account WHERE name = 'bob'").fetchone()[0]
print(f"alice: {alice} cents, bob: {bob} cents")
assert (alice, bob) == (7_000, 8_000)
assert total_cents() == before, "a transfer must never change the bank total"
```

---

## 4. Why tables, and not one big spreadsheet

The relational model says: store each fact **once**, in the table it belongs to,
and join when you need it together.

If you copy Alice's city onto every one of her orders and she moves house, you
now have many places to update and many chances to miss one. A missed row is not
a typo - it is a second, contradictory version of the truth, and the data cannot
tell you which one is right.

```python
orders = [
    {"id": 1, "customer": "alice", "city": "Dublin"},
    {"id": 2, "customer": "alice", "city": "Dublin"},
    {"id": 3, "customer": "alice", "city": "Cork"},
]
cities_on_file = {o["city"] for o in orders}
print("cities recorded for ONE customer:", cities_on_file)
assert len(cities_on_file) == 2, "duplication let two versions of the truth coexist"
print("Which is right? Nothing in the data can say. That is the bug.")
```

---

## 5. Predict before you run

Run the failing transfer again, but delete the `db.rollback()` line. Does Bob
get the money? Does Alice lose it? Which of the two updates survives - the
first, the second, or neither?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every money movement you have ever made ran inside a transaction like the one
above. The reason your bank balance is never briefly wrong by $3,000 is not
careful application code - it is the database refusing to show anybody a
half-finished change.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
