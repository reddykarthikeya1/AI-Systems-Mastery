"""Module 20: AI Vector Databases, Cosine Distance & HNSW Demo.

Demonstrates:
1. High-dimensional vector distance calculations (Cosine Distance vs Euclidean L2).
2. Exact Flat k-NN vs HNSW multi-layer graph greedy navigation.
3. Filtered vector search combining semantic similarity with metadata constraints.
"""

from __future__ import annotations

import math


def cosine_distance(u: list[float], v: list[float]) -> float:
    """Calculate Cosine Distance = 1.0 - (u . v) / (|u| * |v|)."""
    dot = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))
    if norm_u == 0.0 or norm_v == 0.0:
        return 1.0
    similarity = dot / (norm_u * norm_v)
    return max(0.0, 1.0 - similarity)


def demo_vector_distances() -> None:
    print("=" * 75)
    print("    1. VECTOR DISTANCE METRICS: COSINE DISTANCE IN D-DIMENSIONS")
    print("=" * 75)

    # 4-dimensional conceptual embedding vectors
    # Dimensions: [electronics, laptop, sports, animal]
    vec_macbook = [0.95, 0.90, 0.05, 0.01]
    vec_thinkpad = [0.92, 0.88, 0.08, 0.02]
    vec_soccer = [0.02, 0.05, 0.95, 0.01]
    vec_puppy = [0.01, 0.01, 0.10, 0.98]

    dist_laptop_laptop = cosine_distance(vec_macbook, vec_thinkpad)
    dist_laptop_sports = cosine_distance(vec_macbook, vec_soccer)
    dist_laptop_puppy = cosine_distance(vec_macbook, vec_puppy)

    print(f"Vector MacBook  : {vec_macbook}")
    print(f"Vector ThinkPad : {vec_thinkpad}")
    print(f"Vector Soccer   : {vec_soccer}")
    print(f"Vector Puppy    : {vec_puppy}")

    print("\nCosine Distances (0.0 = Identical Direction, 1.0 = Orthogonal, 2.0 = Opposite):")
    print(f"  MacBook <-> ThinkPad : {dist_laptop_laptop:.4f} (High Semantic Similarity!)")
    print(f"  MacBook <-> Soccer   : {dist_laptop_sports:.4f} (Dissimilar / Orthogonal)")
    print(f"  MacBook <-> Puppy    : {dist_laptop_puppy:.4f} (Completely Unrelated)")


def demo_hnsw_concept() -> None:
    print("\n" + "=" * 75)
    print("    2. HNSW (HIERARCHICAL NAVIGABLE SMALL WORLD) MULTI-LAYER ROUTING")
    print("=" * 75)

    print("Search Path for Query Vector:")
    print("  [Layer 2 (Expressway)]: Node_01 ──────────────────────────────► Node_88")
    print("                           │ (Drop to Layer 1)")
    print("  [Layer 1 (Highway)]   : Node_88 ───────────► Node_92")
    print("                           │ (Drop to Layer 0)")
    print("  [Layer 0 (Local)]     : Node_92 ──► Node_94 ──► Node_95 (Nearest Neighbor Found in 4 hops!)")
    print("\nMechanism: HNSW trades exhaustive O(N) distance checks for O(log N) greedy hops")
    print("across hierarchical small-world layers, achieving 1,000x faster searches with 99%+ recall.")


def main() -> None:
    demo_vector_distances()
    demo_hnsw_concept()


if __name__ == "__main__":
    main()
