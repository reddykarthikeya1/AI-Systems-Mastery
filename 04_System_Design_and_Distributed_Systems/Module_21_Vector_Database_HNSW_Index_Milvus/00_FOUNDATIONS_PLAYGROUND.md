# Beginner Playground - Vector Databases and the HNSW Index

> *"A road network. Motorways connect distant cities, local streets connect neighbours. You get close on the motorway and then come off and potter about."*


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

## 1. Exact search, so there is something to compare against

Brute force computes the distance to every vector. It is perfectly accurate and
its cost is the size of the database - which is exactly the property that stops
working.

```python
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
```

---

## 2. Build the local street map

Connect every point to its `M` nearest neighbours. That graph has a useful
property: from anywhere, the neighbour closest to your target is usually a step in
the right direction.

Building it is expensive - this is why adding vectors to an HNSW index costs far
more than appending a row to a table.

```python
M = 8
neighbours = {}
for i, position in POINTS.items():
    others = sorted((j for j in POINTS if j != i),
                    key=lambda j: math.dist(position, POINTS[j]))
    neighbours[i] = others[:M]

print(f"{len(POINTS)} points, {M} neighbours each = "
      f"{len(POINTS) * M:,} edges")
assert all(len(v) == M for v in neighbours.values())
```

---

## 3. Greedy search with a beam

Start somewhere, look at your neighbours, move to whichever is closest to the
query, repeat until nothing is closer.

Pure greedy gets stuck in local minima, so keep a **beam** of the best `ef`
candidates seen so far and explore all of them. `ef` is the knob: larger means
better recall and more work.

```python
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
```

---

## 4. Measure the recall you actually bought

"Approximate" is only acceptable if you know the number. Run many queries, compare
against brute force, and count how often the graph found the true nearest point.

Then raise `ef` and watch recall climb and cost climb with it. That curve *is* the
tuning decision - there is no setting that is simply correct.

```python
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
```

---

## 5. Why HNSW adds layers on top

What you just built is one layer. HNSW stacks several: a sparse top layer whose
few nodes have long-range links, and progressively denser layers below.

A search starts at the top, crosses most of the space in a handful of hops, then
drops a layer and refines. Motorway, then A-road, then the street. It is the same
idea as a skip list, applied to a graph - which is exactly where the design came
from.

```python
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
```

---

## 6. Predict before you run

Exact nearest-neighbour search on a million vectors compares against all
million. A graph index compares against a few hundred. What do you give up to
get that, and how would you measure how much you gave up?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

HNSW is the default index in Qdrant, Milvus, Weaviate and pgvector. The two
knobs - how many neighbours each node keeps, and how wide the search beam is -
trade recall against latency, and tuning them is most of the operational work.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
