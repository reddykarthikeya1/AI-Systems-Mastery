"""Beginner playground for Module 20 - Vector Databases - pgvector and Qdrant.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------------- 1. Meaning as coordinates
vectors = {
    "king":    [0.90, 0.80, 0.10],
    "queen":   [0.88, 0.75, 0.15],
    "monarch": [0.85, 0.82, 0.12],
    "banana":  [0.10, 0.15, 0.95],
    "mango":   [0.12, 0.10, 0.92],
}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm


print(f"king vs queen : {cosine(vectors['king'], vectors['queen']):.3f}")
print(f"king vs banana: {cosine(vectors['king'], vectors['banana']):.3f}")
assert cosine(vectors["king"], vectors["queen"]) > 0.99
assert cosine(vectors["king"], vectors["banana"]) < 0.5
print("Nothing was told that kings and queens are related. The geometry says so.")


# ------------------------------------------ 2. Search means 'what is nearest'
def nearest(query_vector, k=2):
    scored = [(cosine(query_vector, v), name) for name, v in vectors.items()]
    scored.sort(reverse=True)
    return [name for _, name in scored[:k]]


print("nearest to 'king':  ", nearest(vectors["king"]))
print("nearest to 'banana':", nearest(vectors["banana"]))
assert set(nearest(vectors["king"])) <= {"king", "queen", "monarch"}
assert set(nearest(vectors["banana"])) <= {"banana", "mango"}


# ----------------- 3. Exact search does not scale, and here is the arithmetic
corpus_size = 10_000_000
queries_per_second = 100
dimensions = 768

comparisons = corpus_size * queries_per_second
print(f"exact search: {comparisons:,} comparisons/second")
print(f"             x {dimensions} dimensions = {comparisons * dimensions:,} "
      f"multiply-adds/second")
assert comparisons == 1_000_000_000
print("That is not a tuning problem. It is the wrong algorithm.")


# ------------ 4. Approximate search: trade a little recall for a lot of speed
groups = {
    "royalty": ["king", "queen", "monarch"],
    "fruit": ["banana", "mango"],
}
centroids = {
    name: [sum(vectors[m][d] for m in members) / len(members) for d in range(3)]
    for name, members in groups.items()
}

comparison_count = {"n": 0}


def approximate_nearest(query_vector, k=2):
    best_group = max(centroids, key=lambda g: cosine(query_vector, centroids[g]))
    comparison_count["n"] += len(centroids)
    candidates = groups[best_group]
    comparison_count["n"] += len(candidates)
    scored = sorted(((cosine(query_vector, vectors[m]), m) for m in candidates),
                    reverse=True)
    return [name for _, name in scored[:k]]


comparison_count["n"] = 0
approx = approximate_nearest(vectors["king"])
exact = nearest(vectors["king"])
print("approximate result:", approx, f"({comparison_count['n']} comparisons)")
print("exact result:      ", exact, f"({len(vectors)} comparisons)")
assert approx == exact, "same answer here - and it looked at fewer vectors"
assert comparison_count["n"] <= len(vectors), "and the gap widens with scale"


print()
print("All checks passed.")
