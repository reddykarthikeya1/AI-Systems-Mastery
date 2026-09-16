"""Beginner playground for Module 14 - Cassandra - the Masterless Ring.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# ----------------------------------------------------- 1. A ring with no boss
ring_nodes = ["node_A", "node_B", "node_C", "node_D"]
RING_SIZE = 2 ** 16


def token(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % RING_SIZE


node_positions = sorted((token(n), n) for n in ring_nodes)


def replicas_for(key, count=3):
    position = token(key)
    ordered = [n for pos, n in node_positions if pos >= position]
    ordered += [n for pos, n in node_positions if pos < position]
    return ordered[:count]


for key in ["user:42", "user:99"]:
    print(f"{key} lives on {replicas_for(key)}")
assert len(replicas_for("user:42")) == 3, "N = 3 replicas, chosen by position"


# ---------------------------------------------- 2. Ask few, get stale answers
replica_state = {"node_A": "old", "node_B": "old", "node_C": "old"}
N = 3


def write(value, w):
    targets = list(replica_state)[:w]
    for node in targets:
        replica_state[node] = value
    return targets


def read(r):
    answers = list(replica_state)[-r:]
    return [replica_state[node] for node in answers], answers


written_to = write("new", w=1)
values, asked = read(r=1)
print(f"wrote to {written_to}, read from {asked} -> {values}")
assert 1 + 1 <= N, "W + R = 2, which is NOT greater than N = 3"
assert values == ["old"], "the read missed the write entirely"


# --------------------------------------------- 3. R + W > N forces an overlap
for node in replica_state:
    replica_state[node] = "old"

written_to = write("new", w=2)
values, asked = read(r=2)
overlap = set(written_to) & set(asked)
print(f"wrote to {written_to}, read from {asked}, overlap = {overlap}")
assert 2 + 2 > N, "R + W > N"
assert overlap, "the two sets cannot avoid each other"
assert "new" in values, "so the freshest value is guaranteed to be in the answer"
print("The coordinator returns the newest of what it got. Correct, every time.")


# ----------------------- 4. Last write wins, and the clock you must not trust
def resolve(candidates):
    return max(candidates, key=lambda pair: pair[1])[0]


correct = ("alice@new-address.com", 1_000)            # written second, real time
from_skewed_node = ("alice@old-address.com", 5_000)   # written first, bad clock

print("resolved value:", resolve([correct, from_skewed_node]))
assert resolve([correct, from_skewed_node]) == "alice@old-address.com"
print("The older write won because its node's clock was ahead. Run NTP.")


print()
print("All checks passed.")
