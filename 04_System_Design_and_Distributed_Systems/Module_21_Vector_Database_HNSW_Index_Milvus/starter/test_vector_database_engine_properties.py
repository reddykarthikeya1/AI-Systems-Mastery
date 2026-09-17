"""Property and performance assertions for Vector Database & HNSW Indexing.

These complement the correctness tests in `test_vector_database_engine.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

import random
import time

import pytest
from vector_database_engine import BruteForceFlatIndex, HNSWIndex

DIM = 24   # small enough that a pure-Python distance loop stays quick


def _corpus(n: int, seed: int = 7) -> list[tuple[str, list[float]]]:
    rng = random.Random(seed)
    return [(f"doc{i}", [rng.gauss(0, 1) for _ in range(DIM)]) for i in range(n)]


@pytest.mark.perf
@pytest.mark.slow
def test_hnsw_beats_brute_force_at_scale() -> None:
    """An ANN index that is not faster than a linear scan has no reason to exist."""
    data = _corpus(700)
    query = data[0][1]

    flat = BruteForceFlatIndex()
    hnsw = HNSWIndex(dim=DIM, ef_construction=100, ef_search=32, random_seed=7)
    for doc_id, vec in data:
        flat.insert(doc_id, vec)
        hnsw.insert(doc_id, vec)

    def timed(index, repeats: int = 30) -> float:
        best = float("inf")
        for _ in range(repeats):
            start = time.perf_counter()
            index.search(query, top_k=10)
            best = min(best, time.perf_counter() - start)
        return best

    flat_ms = timed(flat) * 1000
    hnsw_ms = timed(hnsw) * 1000

    assert hnsw_ms < flat_ms, (
        f"HNSW {hnsw_ms:.2f} ms vs brute force {flat_ms:.2f} ms at 700 vectors. "
        "The graph walk must beat the linear scan or the index is pointless."
    )


@pytest.mark.perf
@pytest.mark.slow
def test_hnsw_recall_against_exact_search_is_acceptable() -> None:
    """Speed at the cost of unmeasured recall is not a trade, it is a bug.

    HNSW is *approximate*: it may miss true neighbours. That is acceptable only
    if you know the number. This pins it.
    """
    data = _corpus(500, seed=11)
    flat = BruteForceFlatIndex()
    hnsw = HNSWIndex(dim=DIM, ef_construction=100, ef_search=48, random_seed=11)
    for doc_id, vec in data:
        flat.insert(doc_id, vec)
        hnsw.insert(doc_id, vec)

    hits = total = 0
    for _, query in data[:25]:
        exact = {doc_id for doc_id, _dist, _meta in flat.search(query, top_k=10)}
        approx = {doc_id for doc_id, _dist, _meta in hnsw.search(query, top_k=10)}
        hits += len(exact & approx)
        total += len(exact)

    recall = hits / total
    assert recall >= 0.80, (
        f"recall@10 = {recall:.2%} with ef_search=48. Raise ef_search to trade "
        "latency for recall - but never ship an unmeasured recall."
    )


def test_higher_ef_search_does_not_reduce_recall() -> None:
    """ef_search is the recall/latency knob. More search must not find less."""
    data = _corpus(350, seed=3)
    flat = BruteForceFlatIndex()
    for doc_id, vec in data:
        flat.insert(doc_id, vec)

    def recall_at(ef: int) -> float:
        index = HNSWIndex(dim=DIM, ef_construction=80, ef_search=ef, random_seed=3)
        for doc_id, vec in data:
            index.insert(doc_id, vec)
        hits = total = 0
        for _, query in data[:20]:
            exact = {doc_id for doc_id, _dist, _meta in flat.search(query, top_k=10)}
            approx = {doc_id for doc_id, _d, _m in index.search(query, top_k=10)}
            hits += len(exact & approx)
            total += len(exact)
        return hits / total

    assert recall_at(64) >= recall_at(8) - 0.05


def test_searching_an_empty_index_returns_nothing() -> None:
    assert HNSWIndex(dim=DIM).search([0.0] * DIM, top_k=5) == []


def test_top_k_larger_than_the_corpus_is_clamped() -> None:
    index = HNSWIndex(dim=DIM, random_seed=5)
    for doc_id, vec in _corpus(4):
        index.insert(doc_id, vec)
    assert len(index.search([0.0] * DIM, top_k=50)) <= 4


def test_exact_query_returns_the_stored_vector_first() -> None:
    """Querying with a vector that is in the index must return it as the top hit."""
    data = _corpus(200, seed=21)
    index = HNSWIndex(dim=DIM, ef_construction=120, ef_search=64, random_seed=21)
    for doc_id, vec in data:
        index.insert(doc_id, vec)
    target_id, target_vec = data[100]
    results = index.search(target_vec, top_k=1)
    assert results and results[0][0] == target_id
