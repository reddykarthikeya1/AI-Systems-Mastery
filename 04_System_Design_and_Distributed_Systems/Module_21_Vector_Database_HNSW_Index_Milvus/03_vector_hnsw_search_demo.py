"""Module 21: Standalone Interactive Demo - Vector Database & HNSW Approximate Nearest Neighbor Search."""

import random

from project_solution.vector_database_engine import (
    BruteForceFlatIndex,
    HNSWIndex,
    ScalarQuantizer8,
)


def generate_cluster_vector(base_vector: list[float], noise_scale: float = 0.1, rng=None) -> list[float]:
    """Generates a synthetic embedding near a base semantic cluster."""
    if rng is None:
        rng = random.Random()
    return [x + rng.gauss(0, noise_scale) for x in base_vector]


def main() -> None:
    print("=" * 80)
    print(" MODULE 21: HIGH-SCALE VECTOR DATABASE & HNSW GRAPH INDEXING")
    print("=" * 80)

    # ---------------------------------------------------------
    # Step 1: Scalar Quantization (SQ8) Compression
    # ---------------------------------------------------------
    print("\n--- 1. Scalar Quantization (SQ8) Memory Optimization ---")
    raw_embedding = [0.125, -0.452, 0.881, 0.003, -0.912, 0.334, 0.771, -0.119]
    quantized = ScalarQuantizer8.quantize(raw_embedding)
    reconstructed = ScalarQuantizer8.dequantize(quantized)

    raw_bytes = len(raw_embedding) * 4  # 4 bytes per float32
    comp_bytes = len(quantized.data)   # 1 byte per uint8
    comp_ratio = raw_bytes / comp_bytes
    mse = sum((a - b) ** 2 for a, b in zip(raw_embedding, reconstructed, strict=False)) / len(raw_embedding)

    print(f" Raw Float32 Vector (first 4):  {[round(x, 4) for x in raw_embedding[:4]]}")
    print(f" Quantized Uint8 Bytes:         {list(quantized.data)}")
    print(f" Reconstructed Vector:          {[round(x, 4) for x in reconstructed[:4]]}")
    print(f" Memory Compression Ratio:      {comp_ratio:.1f}x (from {raw_bytes}B down to {comp_bytes}B)")
    print(f" Quantization Distortion (MSE): {mse:.6f}")

    # ---------------------------------------------------------
    # Step 2: HNSW Proximity Graph Indexing & Topology
    # ---------------------------------------------------------
    print("\n--- 2. Building Multi-Layer HNSW Proximity Graph ---")
    dim = 16
    rng = random.Random(42)
    hnsw = HNSWIndex(dim=dim, metric="cosine", M=8, ef_construction=32, ef_search=16, random_seed=42)
    flat = BruteForceFlatIndex(metric="cosine")

    # Semantic centers
    center_ai = [1.0 if i % 2 == 0 else 0.0 for i in range(dim)]
    center_db = [0.0 if i % 2 == 0 else 1.0 for i in range(dim)]
    center_music = [0.5 for _ in range(dim)]

    categories = [
        ("ai", center_ai, 60),
        ("db", center_db, 60),
        ("music", center_music, 60),
    ]

    doc_counter = 0
    for cat_name, center, count in categories:
        for i in range(count):
            doc_id = f"doc_{cat_name}_{i:03d}"
            vec = generate_cluster_vector(center, noise_scale=0.15, rng=rng)
            meta = {
                "category": cat_name,
                "access_tier": "premium" if i % 3 == 0 else "standard",
                "score": rng.randint(50, 100),
            }
            hnsw.insert(doc_id, vec, metadata=meta)
            flat.insert(doc_id, vec, metadata=meta)
            doc_counter += 1

    print(f" Indexed Total Vectors:         {doc_counter}")
    print(f" HNSW Graph Max Level:          {hnsw.max_level}")
    print(f" Top Entry Point Node:          '{hnsw.entry_point}'")
    for lvl in range(hnsw.max_level, -1, -1):
        num_nodes_in_lvl = len(hnsw.layers[lvl])
        print(f"   Layer {lvl}: {num_nodes_in_lvl:3d} nodes participating in skip-graph")

    # ---------------------------------------------------------
    # Step 3: ANN Search Benchmarking vs Ground Truth (Flat Index)
    # ---------------------------------------------------------
    print("\n--- 3. ANN Search Accuracy: HNSW vs Ground Truth Flat Scan ---")
    query_vec = generate_cluster_vector(center_ai, noise_scale=0.08, rng=rng)

    hnsw_results = hnsw.search(query_vec, top_k=5)
    flat_results = flat.search(query_vec, top_k=5)

    hnsw_ids = [r[0] for r in hnsw_results]
    flat_ids = [r[0] for r in flat_results]

    overlap = set(hnsw_ids).intersection(set(flat_ids))
    recall_at_5 = len(overlap) / 5.0

    print(f" HNSW Approximate Top 5: {hnsw_ids}")
    for doc_id, dist, meta in hnsw_results:
        print(f"   - {doc_id:<14} | Cosine Dist: {dist:.4f} | Category: {meta['category']}")

    print(f"\n Ground Truth Exact Top 5: {flat_ids}")
    print(f" Recall@5 Metric:          {recall_at_5 * 100:.1f}% Match with Exact Search")

    # ---------------------------------------------------------
    # Step 4: Hybrid Query Engine (Vector Sim + Metadata Filter)
    # ---------------------------------------------------------
    print("\n--- 4. Hybrid Search: Semantic Vector + Metadata Filtering ---")
    print(" Query: Nearest neighbors WHERE category == 'ai' AND access_tier == 'premium'")

    filtered_results = hnsw.search(
        query_vec,
        top_k=3,
        filter_predicate=lambda m: m.get("category") == "ai" and m.get("access_tier") == "premium",
    )

    for doc_id, dist, meta in filtered_results:
        print(f"   Match: {doc_id:<14} | Dist: {dist:.4f} | Meta: {meta}")

    print("=" * 80)


if __name__ == "__main__":
    main()
