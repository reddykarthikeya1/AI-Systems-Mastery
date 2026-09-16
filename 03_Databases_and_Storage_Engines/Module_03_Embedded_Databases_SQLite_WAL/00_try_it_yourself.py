"""Beginner playground for Module 03 - SQLite and the Write-Ahead Log.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import pathlib
import sqlite3
import tempfile

# ---------------------------------- 1. Why an accountant never uses an eraser
folder = pathlib.Path(tempfile.mkdtemp(prefix="wal_playground_"))
ledger = folder / "ledger.db"

setup = sqlite3.connect(ledger)
mode = setup.execute("PRAGMA journal_mode=WAL").fetchone()[0]
print("journal mode:", mode)
assert mode == "wal", "this database now appends corrections instead of erasing"

setup.execute("CREATE TABLE entry (id INTEGER PRIMARY KEY, note TEXT)")
setup.execute("INSERT INTO entry (note) VALUES ('opening balance')")
setup.commit()


# --------------------------------------- 2. Readers never wait for the writer
writer = sqlite3.connect(ledger, isolation_level=None)
reader = sqlite3.connect(ledger, isolation_level=None)

writer.execute("BEGIN")
writer.execute("INSERT INTO entry (note) VALUES ('sale - pen still on the page')")

seen_now = reader.execute("SELECT COUNT(*) FROM entry").fetchone()[0]
print("rows the reader sees while the writer is mid-transaction:", seen_now)
assert seen_now == 1, "the uncommitted row must be invisible"

writer.execute("COMMIT")
seen_after = reader.execute("SELECT COUNT(*) FROM entry").fetchone()[0]
print("rows the reader sees after the writer commits:", seen_after)
assert seen_after == 2, "once committed, the correction is part of the books"


# ------------------------------------------------ 3. Look at the sidecar file
wal_file = ledger.with_name(ledger.name + "-wal")
print("sidecar file:", wal_file.name, "- exists:", wal_file.exists())
assert wal_file.exists(), "committed changes live here until a checkpoint"

size_before = wal_file.stat().st_size
print("WAL size before checkpoint:", size_before, "bytes")
assert size_before > 0


# ----------------------------------- 4. Checkpoint - the end-of-month tidy-up
writer.close()
reader.close()
setup.execute("PRAGMA wal_checkpoint(TRUNCATE)")

size_after = wal_file.stat().st_size
print("WAL size after checkpoint:", size_after, "bytes")
assert size_after == 0, "TRUNCATE folds the log back in and empties it"

notes = [r[0] for r in setup.execute("SELECT note FROM entry ORDER BY id")]
print("final books:", notes)
assert len(notes) == 2, "nothing was lost in the tidy-up"
setup.close()


# ------------------------------------- 5. The one thing WAL does not give you
pen_a = sqlite3.connect(ledger, isolation_level=None, timeout=0.1)
pen_b = sqlite3.connect(ledger, isolation_level=None, timeout=0.1)
pen_a.execute("BEGIN IMMEDIATE")
pen_a.execute("INSERT INTO entry (note) VALUES ('writer A')")

refused = False
try:
    pen_b.execute("BEGIN IMMEDIATE")
except sqlite3.OperationalError as exc:
    refused = True
    print("second writer refused, exactly as designed:", exc)

assert refused, "two concurrent writers must not both get the pen"
pen_a.execute("COMMIT")
pen_a.close()
pen_b.close()


print()
print("All checks passed.")
