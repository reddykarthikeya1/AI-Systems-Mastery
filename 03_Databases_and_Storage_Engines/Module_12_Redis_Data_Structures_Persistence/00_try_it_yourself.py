"""Beginner playground for Module 12 - Redis - Data Structures and Persistence.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import bisect

# ------------------------------------- 1. Why it is fast, and what that costs
whiteboard = {}
whiteboard["user:1:name"] = "alice"
whiteboard["user:1:visits"] = 0

for _ in range(3):
    whiteboard["user:1:visits"] += 1

print("in-memory state:", whiteboard)
assert whiteboard["user:1:visits"] == 3


# ------------------------------------------ 2. The structures are the feature
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


# ------------------------------- 3. Snapshots: a photograph of the whiteboard
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


# ------------------------------- 4. Append-only file: write down every stroke
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


print()
print("All checks passed.")
