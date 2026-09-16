# Beginner Playground - Redis - Data Structures and Persistence

> *"Redis is a whiteboard: gloriously fast, and wiped by a power cut unless somebody was photographing it or writing down every stroke."*

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
import bisect
```

---

## 1. Why it is fast, and what that costs

Redis keeps everything in RAM and runs commands on a single thread. No disk seek
per lookup, and no locking, because there is nothing to contend with.

Two consequences follow immediately, and both matter:

1. Your dataset must fit in memory.
2. One slow command blocks *everything*. A careless `KEYS *` on a big database
   stops the entire server for the duration.

```python
whiteboard = {}
whiteboard["user:1:name"] = "alice"
whiteboard["user:1:visits"] = 0

for _ in range(3):
    whiteboard["user:1:visits"] += 1

print("in-memory state:", whiteboard)
assert whiteboard["user:1:visits"] == 3
```

---

## 2. The structures are the feature

Redis is not a dictionary of strings. It has lists, sets, hashes and sorted sets,
and picking the right one deletes code from your application.

A leaderboard is the clearest example. With a plain key-value store you fetch
every score and sort them yourself. With a sorted set the ordering *is* the data
structure, and "top 3" costs almost nothing.

```python
class SortedSet:
    def __init__(self):
        self._scores = {}
        self._ordered = []  # (score, member), kept sorted

    def add(self, member, score):
        if member in self._scores:
            old = (self._scores[member], member)
            self._ordered.pop(bisect.bisect_left(self._ordered, old))
        self._scores[member] = score
        bisect.insort(self._ordered, (score, member))

    def top(self, n):
        return [m for _, m in reversed(self._ordered[-n:])]


board = SortedSet()
for player, score in [("ana", 50), ("bo", 90), ("cy", 70), ("di", 95), ("ed", 10)]:
    board.add(player, score)

print("top 3:", board.top(3))
assert board.top(3) == ["di", "bo", "cy"]

board.add("ed", 99)
print("after ed scores 99:", board.top(3))
assert board.top(3) == ["ed", "di", "bo"], "the order maintained itself"
```

---

## 3. Snapshots: a photograph of the whiteboard

**RDB** persistence forks the process and writes the whole dataset to one file,
periodically. Restarting means loading that file - very fast, one compact file.

The catch is in the word *periodically*. Everything written since the last
photograph is gone.

```python
store = {}
snapshot = {}

for i in range(10):
    store[f"key{i}"] = i
    if i == 4:
        snapshot = dict(store)  # the photograph
        print("  snapshot taken, holding", len(snapshot), "keys")

print("keys in memory when the power failed:", len(store))
restored_from_rdb = dict(snapshot)
print("keys after restarting from the snapshot:", len(restored_from_rdb))
lost = set(store) - set(restored_from_rdb)
print("lost:", sorted(lost))
assert len(lost) == 5, "everything written after the photograph is gone"
```

---

## 4. Append-only file: write down every stroke

**AOF** persistence appends every write command to a log. Restarting replays the
log from the beginning, so nothing is lost - at the cost of a bigger file, a
slower restart, and a disk write on the hot path.

The honest default for most people is *both*: AOF for durability, RDB for a fast
restore and an easy backup artefact.

```python
aof_log = []
aof_store = {}
for i in range(10):
    command = ("SET", f"key{i}", i)
    aof_log.append(command)
    aof_store[command[1]] = command[2]

replayed = {}
for _, key, value in aof_log:
    replayed[key] = value

print("commands in the log:", len(aof_log))
print("keys after replaying the log:", len(replayed))
assert replayed == aof_store, "AOF loses nothing"
assert len(replayed) - len(snapshot) == 5, "exactly the writes RDB dropped"

print()
print("| mode | lost on crash | restart | write cost |")
print("| RDB  | since last snapshot | fast | none on the hot path |")
print("| AOF  | nothing (fsync always) | slower | one append per write |")
```

---

## 5. Predict before you run

A snapshot is taken every 5 minutes. The server loses power 4 minutes and 50
seconds after the last one. How much work is gone? Now answer the same question
for a server logging every write as it happens.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Redis being "just a cache" is how people lose data. It is a database whose
durability you configure, and the default configuration is chosen for speed.
If you put something in Redis you cannot rebuild, you must decide which
persistence mode you are running before you find out.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
