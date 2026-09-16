# Beginner Playground - Geospatial Systems and Ride-Sharing Dispatch

> *"Postcodes. You do not measure the distance to every house in the country - you look in this postcode and the ones next to it."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

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
import math
import random
```

---

## 1. Never compute distance to everything

The naive approach computes the distance from the rider to every driver in the
system. With 100,000 drivers that is 100,000 distance calculations per request.

The fix is the same one a postcode makes: put everything in a cell, then look only
in the cells that could possibly contain the answer.

```python
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
```

---

## 2. Put every driver in a cell

Divide the map into a grid and record which cell each driver is in. Updating a
driver's position is now a dictionary operation, and finding candidates is a
lookup rather than a scan.

```python
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
```

---

## 3. The bug: searching only your own cell

Look only in the rider's cell and you will usually be right and occasionally be
badly wrong - specifically whenever the rider is near an edge, which in a dense
city is most of the time.

The symptom is not an error. It is a rider being sent a driver four streets away
while a closer one sits around the corner.

```python
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
```

---

## 4. Correct and fast at the same time

Search the 3x3 block of cells and you get the same answer as brute force, having
looked at a tiny fraction of the drivers.

That is the whole trick behind every "find nearby" feature: cheap indexing to cut
the candidate set, exact arithmetic on what is left.

```python
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
```

---

## 5. Why real systems do not use a square grid

A square grid on a sphere has two problems: cells near the poles are a different
size from cells at the equator, and square cells have corners, so "adjacent" means
two different distances depending on whether you cross an edge or a corner.

Uber's H3 uses hexagons: every neighbour is the same distance away, and there are
six of them instead of eight. Geohash and S2 solve it differently, by mapping the
sphere onto a space-filling curve so nearby points share a prefix - which makes
proximity searchable with a plain string index in any database.

```python
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
```

---

## 6. Predict before you run

You index drivers by grid cell and search only the rider's own cell. A rider
stands one metre from a cell boundary, and the nearest driver is two metres
away on the other side. Does your search find them?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Uber's H3 and the geohash systems behind every 'near me' feature are this
idea with better shaped cells. The neighbour-cell bug in section 3 is real,
common, and only shows up for users near a boundary - which is most of them,
in a city.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
