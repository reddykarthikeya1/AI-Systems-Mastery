# Beginner Playground - LSM Trees, Compaction and DynamoDB

> *"Your desk: new notes go on top of the pile, never filed immediately. Finding something means searching from the top down, and tidying up is a separate job you schedule."*

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

## 1. Writes go on top of the pile

A B-tree write finds the right page and edits it - which means a random seek.
An LSM tree just appends to an in-memory table (the **memtable**). No seek, no
search, no waiting.

When the memtable fills, it is written out whole as a sorted, immutable file: an
**SSTable**. Sequential write, never modified again.

```python
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
```

---

## 2. Reads search newest first

`x` might be in the memtable, or in any SSTable. The engine looks in the newest
place first and stops at the first hit - because the newest copy is the true one.

Reverse that order and you serve deleted and superseded data. This is the single
most important invariant in the whole design.

```python
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
```

---

## 3. Read amplification, and what compaction buys

Every flush adds another file a read may have to check. Writes stayed cheap; reads
got more expensive. That growth is **read amplification**.

**Compaction** merges files together, keeping only the newest value for each key.
Fewer files to search, and the superseded copies finally go away.

```python
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
```

---

## 4. Deleting is also a write

You cannot edit an immutable file, so a delete cannot remove anything. It appends
a **tombstone** - a marker meaning "as of now, this key is gone".

The row is only truly gone after a compaction that passes the grace period. Until
then a delete makes the database *bigger*, and a table full of tombstones is one
of the classic ways to make Cassandra reads collapse.

```python
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
```

---

## 5. Predict before you run

You write `x = 1`, then later `x = 2`, and the two writes ended up in
different files. A read arrives. Which file does it look in first, and what
happens if it looked in the other order?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Cassandra, RocksDB, LevelDB, DynamoDB and most modern key-value engines are
LSM trees. The reason they take writes so fast is the reason their reads get
slower over time - and compaction is the bill arriving.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
