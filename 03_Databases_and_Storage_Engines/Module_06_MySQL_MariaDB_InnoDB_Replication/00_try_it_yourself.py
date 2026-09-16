"""Beginner playground for Module 06 - MySQL, InnoDB and Replication.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------------ 1. What actually crosses the wire
primary_rows = {"widget": 100, "gadget": 200}
replica_rows = dict(primary_rows)
binlog = []
replica_position = 0
server_clock = {"tick": 0}

print("primary:", primary_rows)
print("replica:", replica_rows)
assert primary_rows == replica_rows, "they start identical"


# ------------------------------ 2. Replaying deterministic statements is safe
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


# --------------------------------------------- 3. Now the statement that lies
run_on_primary(("stamp_with_server_time", "widget"))
replica_catches_up()

print("primary:", primary_rows)
print("replica:", replica_rows)
assert primary_rows != replica_rows, "the same statement produced different data"
print("This is called replication drift, and it is silent.")


# --------------------------------- 4. Row-based logging removes the guesswork
corrected = ("set_price", ("widget", primary_rows["widget"]))
binlog.append(corrected)
replica_catches_up()

print("after shipping the VALUE instead of the statement:")
print("  primary:", primary_rows)
print("  replica:", replica_rows)
assert primary_rows == replica_rows, "row-based logging cannot drift"


# ---------------------------- 5. Lag is not a failure, it is the normal state
run_on_primary(("set_price", ("gadget", 999)))
print("user just wrote gadget = 999 and the primary said OK")
print("  reading from the primary:", primary_rows["gadget"])
print("  reading from the replica:", replica_rows["gadget"])
assert primary_rows["gadget"] == 999
assert replica_rows["gadget"] != 999, "the replica has not caught up yet"

replica_catches_up()
assert replica_rows["gadget"] == 999, "it gets there - just not instantly"
print("Rule: a read that must see its own write goes to the primary.")


print()
print("All checks passed.")
