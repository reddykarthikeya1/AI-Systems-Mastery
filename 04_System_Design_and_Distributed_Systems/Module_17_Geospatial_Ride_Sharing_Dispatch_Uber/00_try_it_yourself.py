"""Beginner playground for Module 17 - Geospatial Systems and Ride-Sharing Dispatch.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math
import random

# ------------------------------------ 1. Never compute distance to everything
random.seed(17)
drivers = {f"driver{i}": (random.uniform(0, 100), random.uniform(0, 100))
           for i in range(100_000)}
distance_calls = {"count": 0}


def distance(a, b):
    distance_calls["count"] += 1
    return math.hypot(a[0] - b[0], a[1] - b[1])


rider = (50.2, 50.3)
distance_calls["count"] = 0
nearest_brute = min(drivers, key=lambda d: distance(rider, drivers[d]))
brute_calls = distance_calls["count"]
print(f"brute force: {brute_calls:,} distance calculations")
assert brute_calls == 100_000


# ---------------------------------------------- 2. Put every driver in a cell
CELL_SIZE = 1.0


def cell_of(point):
    return (int(point[0] // CELL_SIZE), int(point[1] // CELL_SIZE))


grid = {}
for name, position in drivers.items():
    grid.setdefault(cell_of(position), []).append(name)

print(f"{len(grid):,} occupied cells, "
      f"average {len(drivers) / len(grid):.0f} drivers each")
assert len(grid) > 1_000
assert sum(len(v) for v in grid.values()) == 100_000


# ----------------------------------- 3. The bug: searching only your own cell
def nearest_one_cell(point):
    candidates = grid.get(cell_of(point), [])
    if not candidates:
        return None
    return min(candidates, key=lambda d: distance(point, drivers[d]))


def nearest_with_neighbours(point):
    cx, cy = cell_of(point)
    candidates = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            candidates += grid.get((cx + dx, cy + dy), [])
    return min(candidates, key=lambda d: distance(point, drivers[d]))


edge_rider = (50.99, 50.99)                 # right up against a cell corner
one_cell = nearest_one_cell(edge_rider)
nine_cells = nearest_with_neighbours(edge_rider)

distance_calls["count"] = 0
d_one = distance(edge_rider, drivers[one_cell])
d_nine = distance(edge_rider, drivers[nine_cells])
print(f"searching 1 cell : {one_cell} at {d_one:.4f}")
print(f"searching 9 cells: {nine_cells} at {d_nine:.4f}")
assert d_nine <= d_one, "the 3x3 search can only ever do better"


# --------------------------------------- 4. Correct and fast at the same time
distance_calls["count"] = 0
grid_answer = nearest_with_neighbours(rider)
grid_calls = distance_calls["count"]

distance_calls["count"] = 0
brute_answer = min(drivers, key=lambda d: distance(rider, drivers[d]))

print(f"grid search:  {grid_calls:>7,} distance calculations -> {grid_answer}")
print(f"brute force:  {brute_calls:>7,} distance calculations -> {brute_answer}")
print(f"speed-up: {brute_calls / grid_calls:.0f}x for an identical answer")
assert grid_answer == brute_answer, "same driver, far less work"
assert grid_calls < brute_calls / 100


# ------------------------------- 5. Why real systems do not use a square grid
def geohash_like(point, precision=6):
    # Interleave the bits of x and y so that a shared prefix means proximity.
    x, y = int(point[0] * 100), int(point[1] * 100)
    bits = "".join(f"{(x >> i) & 1}{(y >> i) & 1}" for i in reversed(range(16)))
    return bits[:precision]


near_a, near_b = (50.20, 50.30), (50.21, 50.30)
far = (12.0, 88.0)
print("two nearby points:", geohash_like(near_a), geohash_like(near_b))
print("a distant point:  ", geohash_like(far))
assert geohash_like(near_a) == geohash_like(near_b), "neighbours share a prefix"
assert geohash_like(far) != geohash_like(near_a)
print("Prefix match = proximity search, using an ordinary string index.")


print()
print("All checks passed.")
