"""Beginner playground for Module 09 - Consistent Hashing and Distributed Partitioning.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import bisect
import hashlib

# ----------------------------------- 1. The obvious way, and why it collapses
KEYS = [f"user:{i}" for i in range(20_000)]


def stable_hash(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16)


def modulo_placement(key, servers):
    return stable_hash(key) % servers


before = {k: modulo_placement(k, 4) for k in KEYS}
after = {k: modulo_placement(k, 5) for k in KEYS}
moved = sum(1 for k in KEYS if before[k] != after[k])

print(f"adding a 5th server moved {moved:,} of {len(KEYS):,} keys "
      f"({moved / len(KEYS):.0%})")
assert moved / len(KEYS) > 0.75, "adding one server rehomed most of the data"
print("Ideally we would move 1/5 of them. We moved four times that.")


# --------------------------------------------------------------- 2. The wheel
RING = 2 ** 32


class HashRing:
    def __init__(self, servers, vnodes=1):
        self.vnodes = vnodes
        self.ring = {}
        for server in servers:
            self.add(server)

    def add(self, server):
        for v in range(self.vnodes):
            self.ring[stable_hash(f"{server}#{v}") % RING] = server
        self.sorted_points = sorted(self.ring)

    def remove(self, server):
        self.ring = {p: s for p, s in self.ring.items() if s != server}
        self.sorted_points = sorted(self.ring)

    def server_for(self, key):
        point = stable_hash(key) % RING
        index = bisect.bisect_left(self.sorted_points, point)
        if index == len(self.sorted_points):
            index = 0                                # wrapped past 12 o'clock
        return self.ring[self.sorted_points[index]]


ring = HashRing(["s1", "s2", "s3", "s4"])
print("user:1 lives on", ring.server_for("user:1"))
assert ring.server_for("user:1") == ring.server_for("user:1"), "placement is stable"


# ------------------------------ 3. Add a server and count what actually moves
ring_before = {k: ring.server_for(k) for k in KEYS}
ring.add("s5")
ring_after = {k: ring.server_for(k) for k in KEYS}
ring_moved = sum(1 for k in KEYS if ring_before[k] != ring_after[k])

print(f"modulo hashing moved:     {moved / len(KEYS):>6.1%} of keys")
print(f"consistent hashing moved: {ring_moved / len(KEYS):>6.1%} of keys")
assert ring_moved < moved / 3, "an order of magnitude less data movement"
print("Everything that did move went to the new server. Nothing else shifted.")


# ------------------------------ 4. Virtual nodes: the fix for the lumpy wheel
def spread(vnodes):
    test_ring = HashRing(["s1", "s2", "s3", "s4"], vnodes=vnodes)
    counts = dict.fromkeys(["s1", "s2", "s3", "s4"], 0)
    for key in KEYS:
        counts[test_ring.server_for(key)] += 1
    return counts


one_point = spread(1)
many_points = spread(150)
imbalance_1 = max(one_point.values()) / min(one_point.values())
imbalance_150 = max(many_points.values()) / min(many_points.values())

print("1 point per server:  ", one_point, f"-> {imbalance_1:.2f}x imbalance")
print("150 points per server:", many_points, f"-> {imbalance_150:.2f}x imbalance")
assert imbalance_150 < imbalance_1, "virtual nodes smooth the arcs out"
assert imbalance_150 < 1.25, "close enough to even for production"


print()
print("All checks passed.")
