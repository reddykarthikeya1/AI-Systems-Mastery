"""Beginner playground for Module 21 - Vector Databases and the HNSW Index.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math
import random

# ------------------ 1. Exact search, so there is something to compare against
random.seed(21)
POINTS = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(800)}
comparisons = {"count": 0}


def distance(a, b):
    comparisons["count"] += 1
    return math.hypot(a[0] - b[0], a[1] - b[1])


def brute_force(query):
    comparisons["count"] = 0
    best = min(POINTS, key=lambda i: distance(query, POINTS[i]))
    return best, comparisons["count"]


query_point = (50.0, 50.0)
exact_id, exact_cost = brute_force(query_point)
print(f"brute force: point {exact_id} after {exact_cost} comparisons")
assert exact_cost == len(POINTS)


# ---------------------------------------------- 2. Build the local street map
M = 8
neighbours = {}
for i, position in POINTS.items():
    others = sorted((j for j in POINTS if j != i),
                    key=lambda j: math.dist(position, POINTS[j]))
    neighbours[i] = others[:M]

print(f"{len(POINTS)} points, {M} neighbours each = "
      f"{len(POINTS) * M:,} edges")
assert all(len(v) == M for v in neighbours.values())


# ----------------------------------------------- 3. Greedy search with a beam
def graph_search(query, ef=10, entry=0):
    comparisons["count"] = 0
    visited = {entry}
    candidates = [(distance(query, POINTS[entry]), entry)]
    best = list(candidates)
    while candidates:
        candidates.sort()
        current_distance, current = candidates.pop(0)
        if current_distance > max(d for d, _ in best) and len(best) >= ef:
            break
        for neighbour in neighbours[current]:
            if neighbour in visited:
                continue
            visited.add(neighbour)
            d = distance(query, POINTS[neighbour])
            candidates.append((d, neighbour))
            best.append((d, neighbour))
            best.sort()
            best = best[:ef]
    return best[0][1], comparisons["count"]


found, graph_cost = graph_search(query_point)
print(f"graph search: point {found} after {graph_cost} comparisons")
print(f"brute force:  point {exact_id} after {exact_cost} comparisons")
print(f"{exact_cost / graph_cost:.1f}x fewer distance calculations")
assert graph_cost < exact_cost / 3


# ---------------------------------- 4. Measure the recall you actually bought
def measure(ef, trials=100):
    random.seed(99)
    hits = 0
    total_cost = 0
    for _ in range(trials):
        q = (random.uniform(0, 100), random.uniform(0, 100))
        truth, _ = brute_force(q)
        guess, cost = graph_search(q, ef=ef)
        hits += guess == truth
        total_cost += cost
    return hits / trials, total_cost / trials


print(f"{'ef':>4} {'recall@1':>10} {'comparisons':>14}")
results = {}
for ef in (1, 5, 20, 50):
    recall, cost = measure(ef)
    results[ef] = (recall, cost)
    print(f"{ef:>4} {recall:>9.0%} {cost:>14.0f}")

assert results[50][0] >= results[1][0], "a wider beam never finds less"
assert results[50][1] > results[1][1], "and always costs more"
assert results[50][0] > 0.8, "high recall at a fraction of brute-force cost"
assert results[50][1] < len(POINTS), "still cheaper than checking everything"


# --------------------------------------------- 5. Why HNSW adds layers on top
MULTIPLIER = 16


def layers_for(points):
    # HNSW puts every point on layer 0 and promotes roughly 1 in MULTIPLIER to
    # each layer above, so the layer count grows only logarithmically.
    return max(1, math.ceil(math.log(points, MULTIPLIER)))


for n in (1_000, 1_000_000, 1_000_000_000):
    layers = layers_for(n)
    top = max(1, n // MULTIPLIER ** (layers - 1))
    print(f"  {n:>15,} points -> {layers} layers, top layer holds ~{top:,} nodes")

assert layers_for(1_000_000_000) <= 8, "a billion points needs only a handful of layers"
assert layers_for(1_000) < layers_for(1_000_000_000), "and it grows logarithmically"
print("A tiny top layer crosses the space in a few hops. That is the H in HNSW.")


print()
print("All checks passed.")
