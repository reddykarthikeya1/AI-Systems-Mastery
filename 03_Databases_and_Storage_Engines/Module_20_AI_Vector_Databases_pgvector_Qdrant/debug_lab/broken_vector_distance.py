"""DEBUG LAB: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

import math

def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def cosine(a: list[float], b: list[float]) -> float:
    norm_a = math.sqrt(dot(a, a))
    norm_b = math.sqrt(dot(b, b))
    return dot(a, b) / (norm_a * norm_b)

def reproduce_defect() -> None:
    print("Ranking two candidate embeddings against a query vector...")
    query = [1.0, 0.0]
    candidates = {
        "relevant_but_small_magnitude": [0.9, 0.1],   # nearly the same direction as query
        "irrelevant_but_large_magnitude": [3.0, -2.9],  # very different direction, huge norm
    }

    top_by_dot = max(candidates, key=lambda k: dot(query, candidates[k]))
    top_by_cosine = max(candidates, key=lambda k: cosine(query, candidates[k]))

    print(f"Top match using the index's raw dot product: {top_by_dot}")
    print(f"Top match using cosine similarity (normalized): {top_by_cosine}")
    if top_by_dot != top_by_cosine:
        print("[DEFECT OBSERVED] The index is configured for dot-product similarity "
              "over embeddings inserted with arbitrary magnitudes, so the large, "
              "off-direction vector outranks the genuinely relevant one.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
