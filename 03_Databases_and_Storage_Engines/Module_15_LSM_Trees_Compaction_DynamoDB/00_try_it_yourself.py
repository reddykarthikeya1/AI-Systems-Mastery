"""Beginner playground for Module 15 - LSM Trees, Compaction and DynamoDB.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. Writes go on top of the pile
memtable = {}
sstables = []          # newest last
MEMTABLE_LIMIT = 3


def put(key, value):
    memtable[key] = value
    if len(memtable) >= MEMTABLE_LIMIT:
        flush()


def flush():
    sstables.append(dict(sorted(memtable.items())))
    memtable.clear()


for key, value in [("a", 1), ("b", 1), ("c", 1), ("x", 1), ("y", 1), ("z", 1)]:
    put(key, value)

print("sstables on disk:", sstables)
print("memtable:", memtable)
assert len(sstables) == 2, "two flushes, two immutable files"


# ----------------------------------------------- 2. Reads search newest first
files_examined = {"count": 0}


def get(key):
    files_examined["count"] += 1
    if key in memtable:
        return memtable[key]
    for table in reversed(sstables):        # newest first - this order is the point
        files_examined["count"] += 1
        if key in table:
            return table[key]
    return None


put("x", 2)                                 # x = 2 now sits in the memtable
print("x in the newest sstable was:", sstables[-1].get("x"))
print("get('x') returns:", get("x"))
assert get("x") == 2, "the newest copy wins"
assert sstables[-1]["x"] == 1, "the old copy is still on disk, untouched"


# ---------------------------- 3. Read amplification, and what compaction buys
for i in range(12):
    put(f"k{i}", i)

files_examined["count"] = 0
get("missing_key")
before = files_examined["count"]
print(f"files touched looking for a missing key: {before} ({len(sstables)} sstables)")


def compact():
    merged = {}
    for table in sstables:                  # oldest first, so newest overwrites
        merged.update(table)
    sstables.clear()
    sstables.append(dict(sorted(merged.items())))


compact()
files_examined["count"] = 0
get("missing_key")
after = files_examined["count"]
print(f"after compaction: {after} ({len(sstables)} sstable)")
assert after < before, "compaction is what keeps reads from degrading forever"
assert sstables[0]["x"] == 2, "compaction kept the newest value, discarded the old"


# ------------------------------------------------ 4. Deleting is also a write
TOMBSTONE = object()


def delete(key):
    put(key, TOMBSTONE)


def get_with_tombstones(key):
    if key in memtable:
        value = memtable[key]
    else:
        value = None
        for table in reversed(sstables):
            if key in table:
                value = table[key]
                break
    return None if value is TOMBSTONE else value


size_before = len(memtable) + sum(len(t) for t in sstables)
delete("x")
size_after = len(memtable) + sum(len(t) for t in sstables)

print("get('x') after deleting:", get_with_tombstones("x"))
print(f"entries stored before the delete: {size_before}, after: {size_after}")
assert get_with_tombstones("x") is None, "the key reads as absent"
assert size_after >= size_before, "deleting made the database no smaller"


print()
print("All checks passed.")
