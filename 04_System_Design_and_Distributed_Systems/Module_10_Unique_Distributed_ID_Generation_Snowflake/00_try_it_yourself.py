"""Beginner playground for Module 10 - Distributed Unique ID Generation (Snowflake).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import time

# ----------------------- 1. Three ways to make an id, and what each one costs
uuid_like = ["c9f0", "1a2b", "7e4d", "03ff"]
print("random ids in creation order:", uuid_like)
print("the same ids sorted:         ", sorted(uuid_like))
assert sorted(uuid_like) != uuid_like, "sort order tells you nothing about time"


# --------------------------------------------- 2. Sixty-four bits, divided up
EPOCH_MS = 1_700_000_000_000
MACHINE_BITS, SEQUENCE_BITS = 10, 12
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1


class Snowflake:
    def __init__(self, machine_id):
        assert 0 <= machine_id < (1 << MACHINE_BITS)
        self.machine_id = machine_id
        self.last_ms = -1
        self.sequence = 0

    def next_id(self, now_ms):
        if now_ms < self.last_ms:
            raise RuntimeError("clock moved backwards; refusing to issue an id")
        if now_ms == self.last_ms:
            self.sequence += 1
            if self.sequence > MAX_SEQUENCE:
                raise RuntimeError("4096 ids in one millisecond; wait for the next")
        else:
            self.sequence = 0
        self.last_ms = now_ms
        return (((now_ms - EPOCH_MS) << (MACHINE_BITS + SEQUENCE_BITS))
                | (self.machine_id << SEQUENCE_BITS)
                | self.sequence)


generator = Snowflake(machine_id=7)
ids = [generator.next_id(now_ms=EPOCH_MS + 1_000) for _ in range(3)]
print("three ids from one machine in one millisecond:", ids)
assert ids == sorted(ids), "the sequence field keeps them ordered within the ms"
assert len(set(ids)) == 3


# ------------------------------ 3. Two machines, no conversation between them
machine_a = Snowflake(machine_id=1)
machine_b = Snowflake(machine_id=2)
same_instant = EPOCH_MS + 5_000

batch_a = {machine_a.next_id(same_instant) for _ in range(1_000)}
batch_b = {machine_b.next_id(same_instant) for _ in range(1_000)}

print(f"machine 1 issued {len(batch_a):,} ids, machine 2 issued {len(batch_b):,}")
print("overlap:", len(batch_a & batch_b))
assert batch_a & batch_b == set(), "collision is impossible, not merely unlikely"
assert len(batch_a | batch_b) == 2_000


# ------------------------ 4. Unpacking an id, and the failure you must handle
def unpack(snowflake_id):
    sequence = snowflake_id & MAX_SEQUENCE
    machine = (snowflake_id >> SEQUENCE_BITS) & ((1 << MACHINE_BITS) - 1)
    timestamp = (snowflake_id >> (MACHINE_BITS + SEQUENCE_BITS)) + EPOCH_MS
    return timestamp, machine, sequence


sample = Snowflake(machine_id=42).next_id(EPOCH_MS + 9_876)
timestamp, machine, sequence = unpack(sample)
print(f"id {sample} -> t+{timestamp - EPOCH_MS} ms, machine {machine}, seq {sequence}")
assert (machine, sequence) == (42, 0)
assert timestamp == EPOCH_MS + 9_876

clock_skewed = Snowflake(machine_id=3)
clock_skewed.next_id(EPOCH_MS + 10_000)
try:
    clock_skewed.next_id(EPOCH_MS + 9_000)      # NTP stepped the clock back
    raise AssertionError("it should have refused")
except RuntimeError as exc:
    print("clock went backwards ->", exc)

print("Refusing to issue is correct. Issuing a duplicate id is unrecoverable.")
print("(time.time() is available here too:", int(time.time()) > 0, ")")


print()
print("All checks passed.")
