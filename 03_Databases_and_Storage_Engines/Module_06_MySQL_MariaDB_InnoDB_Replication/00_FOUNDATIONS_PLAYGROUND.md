# Beginner Playground - MySQL, InnoDB and Replication

> *"Replication does not photocopy the database. It posts a list of instructions and trusts the other end to follow them identically - which is where it gets interesting."*


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

## 1. What actually crosses the wire

A replica does not receive database *files*. It receives a **binary log** - an
ordered list of changes - and applies them in order. Catching up is just
replaying entries you have not reached yet.

Two ways to write that log, and the difference is the whole module:

- **Statement-based**: log the SQL. Compact, but the replica re-*executes* it.
- **Row-based**: log the resulting row values. Bulkier, but there is nothing left
  to interpret.

```python
primary_rows = {"widget": 100, "gadget": 200}
replica_rows = dict(primary_rows)
binlog = []
replica_position = 0
server_clock = {"tick": 0}

print("primary:", primary_rows)
print("replica:", replica_rows)
assert primary_rows == replica_rows, "they start identical"
```

---

## 2. Replaying deterministic statements is safe

`raise every price by 10%` means exactly one thing. Run it on the same starting
data anywhere in the world and you get the same answer. Statements like this
replicate perfectly.

```python
def apply_statement(rows, statement):
    kind, arg = statement
    if kind == "raise_all_by_percent":
        for key in list(rows):
            rows[key] = int(rows[key] * (100 + arg) / 100)
    elif kind == "set_price":
        name, value = arg
        rows[name] = value
    elif kind == "stamp_with_server_time":
        server_clock["tick"] += 1
        rows[arg] = server_clock["tick"]
    else:
        raise ValueError(kind)


def run_on_primary(statement):
    apply_statement(primary_rows, statement)
    binlog.append(statement)


def replica_catches_up():
    global replica_position
    while replica_position < len(binlog):
        apply_statement(replica_rows, binlog[replica_position])
        replica_position += 1


run_on_primary(("raise_all_by_percent", 10))
replica_catches_up()
print("after a 10% rise -> primary:", primary_rows, " replica:", replica_rows)
assert primary_rows == replica_rows, "deterministic statements replay perfectly"
```

---

## 3. Now the statement that lies

`stamp_with_server_time` is a stand-in for `NOW()`, `RAND()`, `UUID()`, or
`CONNECTION_ID()`. The primary evaluates it at one moment; the replica evaluates
it again, later, and gets a different answer.

Nothing errors. Nothing is logged. The two databases simply stop agreeing, and
you find out weeks later when a report does not reconcile.

```python
run_on_primary(("stamp_with_server_time", "widget"))
replica_catches_up()

print("primary:", primary_rows)
print("replica:", replica_rows)
assert primary_rows != replica_rows, "the same statement produced different data"
print("This is called replication drift, and it is silent.")
```

---

## 4. Row-based logging removes the guesswork

Log the *result* instead of the recipe: "widget is now 1". There is nothing left
for the replica to evaluate differently. This is why row-based logging is the
modern default.

```python
corrected = ("set_price", ("widget", primary_rows["widget"]))
binlog.append(corrected)
replica_catches_up()

print("after shipping the VALUE instead of the statement:")
print("  primary:", primary_rows)
print("  replica:", replica_rows)
assert primary_rows == replica_rows, "row-based logging cannot drift"
```

---

## 5. Lag is not a failure, it is the normal state

Replication is asynchronous by default: the primary commits and tells the client
"done" *before* the replica has heard anything. For that window - usually
milliseconds, occasionally minutes - the replica is a view of the past.

So "write to the primary, immediately read from a replica" is a broken pattern,
not a flaky one.

```python
run_on_primary(("set_price", ("gadget", 999)))
print("user just wrote gadget = 999 and the primary said OK")
print("  reading from the primary:", primary_rows["gadget"])
print("  reading from the replica:", replica_rows["gadget"])
assert primary_rows["gadget"] == 999
assert replica_rows["gadget"] != 999, "the replica has not caught up yet"

replica_catches_up()
assert replica_rows["gadget"] == 999, "it gets there - just not instantly"
print("Rule: a read that must see its own write goes to the primary.")
```

---

## 6. Predict before you run

The replica is told to run the *exact same statement* as the primary. Can
running an identical statement on identical data ever produce a different
result? Name one SQL expression that would do it.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

"The replica says the order is not there, but I just placed it" is a support
ticket you will see. It is not a bug - it is replication lag, and the fix is
architectural: route reads that must see their own writes to the primary.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
