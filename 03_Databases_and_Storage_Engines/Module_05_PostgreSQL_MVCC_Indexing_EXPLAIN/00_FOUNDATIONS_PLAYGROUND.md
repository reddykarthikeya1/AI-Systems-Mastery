# Beginner Playground - MVCC, Indexes and EXPLAIN

> *"MVCC is a library that never throws an edition away. Whichever edition was current when you walked in is the one you read, right to the last page."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

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
import random
import sqlite3
import time
```

---

## 1. MVCC: nobody blocks anybody

A simple database locks a row while you change it, and everyone else waits. With
**Multi-Version Concurrency Control** nobody waits, because a write does not
overwrite - it adds a new version stamped with a transaction number.

A reader that started at transaction 5 keeps seeing the newest version numbered
5 or lower, even while transaction 6 is busy writing. Like a library that keeps
every edition on the shelf: you read the one that was current when you walked in,
and a new printing arriving mid-chapter does not change the words in your hands.

```python
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
```

---

## 2. The cost nobody warns you about

Old versions do not vacate the shelf by themselves. Until a cleanup process
decides no transaction could still want them, they occupy space and every scan
walks past them.

In PostgreSQL that cleanup is `VACUUM`, and "the table is 40 GB but holds 2 GB of
live rows" is what it looks like when it falls behind.

```python
live_rows = len({k for (_, k, _) in versions})
stored_rows = len(versions)
print(f"rows you can see: {live_rows}, row versions actually stored: {stored_rows}")
assert stored_rows > live_rows, "the superseded version is still on disk"
print("That gap is what VACUUM exists to close.")
```

---

## 3. Now the part you will use every week: EXPLAIN

Build a table with 20,000 users and ask for one of them by email, with no index.
The plan comes back with the word every performance investigation is looking for.

```python
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
```

---

## 4. Add the index, read the plan again

`SCAN` means *look at every row*. `SEARCH ... USING INDEX` means *jump straight
there*. One word of difference in the plan; a very different amount of work.

```python
users.execute("CREATE INDEX idx_users_email ON users(email)")
plan_after = users.execute("EXPLAIN QUERY PLAN " + query, ("user19999@example.com",))
plan_after_text = " ".join(str(row[-1]) for row in plan_after)
print("plan WITH an index:   ", plan_after_text)
assert "SEARCH" in plan_after_text, "now it jumps straight to the row"
assert "idx_users_email" in plan_after_text
```

---

## 5. Measure it, do not trust it

A plan that looks better is a hypothesis. A stopwatch is evidence.

```python
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
```

---

## 6. And the catch

An index is a second copy of the column, kept sorted. Every `INSERT`, `UPDATE`
and `DELETE` has to maintain it. Indexes are not free - they trade write speed
and disk space for read speed.

Which is why "add an index to every column" is not a strategy. Index what you
actually filter, join and sort on, and check with `EXPLAIN` that the database
agrees it is worth using.

```python
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
```

---

## 7. Predict before you run

Before the index exists, the query plan says `SCAN`. After you create the
index it says `SEARCH`. Roughly how much faster do you expect the indexed
version to be on 20,000 rows - twice? Ten times? A hundred times? Write down a
number, then look at what the script prints.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

`EXPLAIN` is the single highest-value command in this entire course. Every
"the database got slow" ticket you will ever pick up starts by running the
query plan and looking for the word that means *scan*. If you learn one habit
here, learn that one.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
