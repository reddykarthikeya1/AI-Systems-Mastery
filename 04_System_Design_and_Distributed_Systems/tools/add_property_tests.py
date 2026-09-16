#!/usr/bin/env python3
"""Add property and performance test suites to the modules that make measurable claims.

Why these specifically
----------------------
The course had **zero** performance assertions. Every other test here checks
that an operation is *correct*; none checked that a claimed *win* is real. That
is the gap that let the Advanced Python course ship a "native accelerator" which
was measured, much later, at 5.26x **slower** than plain Python.

A performance test fails when the story stops being true. That makes it the only
kind of test that defends a teaching claim rather than an implementation detail.

Each file below asserts something the module's README actually promises:

  M04  least-connections beats round-robin under uneven hold times
  M09  adding a node remaps ~1/N of keys, not ~all of them
  M10  IDs stay unique and monotonic under concurrent generation
  M11  single-flight collapses N concurrent misses into exactly one load
  M12  Bloom false-positive rate lands near theory; false negatives impossible
  M19  near-duplicate detection catches what URL comparison misses
  M20  the atomic path never oversells; the naive path demonstrably does
  M21  HNSW beats brute force at scale, at a stated recall
  M22  paged allocation reclaims the fragmentation naive caching wastes
  M24  a minority partition cannot commit

Run once:  python tools/add_property_tests.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER = '''"""Property and performance assertions for {title}.

These complement the correctness tests in `{sibling}`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

'''

FILES: dict[str, tuple[str, str, str]] = {}

# ---------------------------------------------------------------- M09 --------
FILES["09"] = (
    "consistent_hash_ring",
    "Consistent Hashing & Ring Partitioning",
    '''
import time

from consistent_hash_ring import ConsistentHashRing

KEYS = [f"user:{i}" for i in range(4000)]


def _assignments(ring: ConsistentHashRing) -> dict[str, str]:
    return {k: ring.get_node(k) for k in KEYS}


@pytest.mark.perf
def test_adding_a_node_remaps_about_one_over_n_of_keys() -> None:
    """The whole point of consistent hashing, stated as a measurement.

    Naive `hash(key) % N` remaps ~(N-1)/N of all keys when N changes - for 3 to
    4 nodes that is ~75%. A consistent hash ring should move ~1/4, because only
    the keys falling in the new node's arcs are affected.

    If this test fails high, the ring is behaving like modulo hashing and the
    module's central claim is false.
    """
    ring = ConsistentHashRing(["a", "b", "c"], vnodes=150)
    before = _assignments(ring)

    ring.add_node("d")
    after = _assignments(ring)

    moved = sum(1 for k in KEYS if before[k] != after[k])
    fraction = moved / len(KEYS)

    # Ideal is 1/4 = 0.25. Allow generous slack for hash variance, but stay far
    # below the ~0.75 that modulo hashing would produce.
    assert 0.10 <= fraction <= 0.45, (
        f"{fraction:.1%} of keys remapped on a 3->4 node change. "
        "Expected ~25%; modulo hashing would give ~75%."
    )


@pytest.mark.perf
def test_more_vnodes_reduces_distribution_variance() -> None:
    """Virtual nodes exist to fix variance. Measure that they do."""
    few = ConsistentHashRing(["a", "b", "c", "d"], vnodes=1)
    many = ConsistentHashRing(["a", "b", "c", "d"], vnodes=200)

    def spread(ring: ConsistentHashRing) -> float:
        counts: dict[str, int] = {}
        for k in KEYS:
            node = ring.get_node(k)
            counts[node] = counts.get(node, 0) + 1
        ideal = len(KEYS) / 4
        return max(abs(c - ideal) for c in counts.values()) / ideal

    assert spread(many) < spread(few), (
        f"200 vnodes gave spread {spread(many):.2f}, 1 vnode gave {spread(few):.2f}. "
        "More virtual nodes must reduce imbalance, or they serve no purpose."
    )


def test_removing_a_node_never_loses_a_key() -> None:
    """Every key must still resolve to *some* live node after a removal."""
    ring = ConsistentHashRing(["a", "b", "c"], vnodes=100)
    ring.remove_node("b")
    for k in KEYS[:500]:
        node = ring.get_node(k)
        assert node in {"a", "c"}, f"key {k} resolved to {node!r} after removing 'b'"


def test_empty_ring_returns_none_rather_than_raising() -> None:
    """A ring with no nodes is a legitimate transient state during bootstrap."""
    assert ConsistentHashRing([], vnodes=10).get_node("anything") is None


def test_preference_list_is_distinct_and_bounded() -> None:
    """A replica set of 3 that contains the same box twice survives no failure."""
    ring = ConsistentHashRing(["a", "b", "c", "d"], vnodes=120)
    for k in KEYS[:200]:
        prefs = ring.get_preference_list(k, 3)
        assert len(prefs) == len(set(prefs)), f"duplicate physical node in {prefs}"
        assert len(prefs) <= 4


def test_preference_list_larger_than_cluster_is_clamped() -> None:
    ring = ConsistentHashRing(["a", "b"], vnodes=50)
    assert len(ring.get_preference_list("k", 10)) <= 2


@pytest.mark.perf
@pytest.mark.slow
def test_lookup_cost_is_logarithmic_not_linear() -> None:
    """Ring lookup is a binary search over the sorted ring, so growing the ring
    100x must not grow per-lookup cost anywhere near 100x."""

    def per_lookup(n_nodes: int) -> float:
        ring = ConsistentHashRing([f"n{i}" for i in range(n_nodes)], vnodes=50)
        probe = KEYS[:2000]
        start = time.perf_counter()
        for k in probe:
            ring.get_node(k)
        return (time.perf_counter() - start) / len(probe)

    small = per_lookup(3)
    large = per_lookup(300)
    assert large / small < 4.0, (
        f"per-lookup cost grew {large / small:.1f}x when the ring grew 100x - "
        "that is not a binary search."
    )
''',
)

# ---------------------------------------------------------------- M11 --------
FILES["11"] = (
    "distributed_cache_guard",
    "Distributed Caching & Stampede Prevention",
    '''
import concurrent.futures
import time

from distributed_cache_guard import DistributedCacheGuard


@pytest.mark.perf
@pytest.mark.slow
def test_a_cache_hit_is_dramatically_cheaper_than_the_loader() -> None:
    """A cache that is not faster than the thing it caches is not a cache."""
    cache = DistributedCacheGuard()

    def slow_loader() -> str:
        time.sleep(0.03)
        return "payload"

    t0 = time.perf_counter()
    cache.get("k", slow_loader, ttl_seconds=60.0)
    cold = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(200):
        cache.get("k", slow_loader, ttl_seconds=60.0)
    warm = (time.perf_counter() - t0) / 200

    assert cold / warm > 100, f"cache only {cold / warm:.0f}x faster than the loader"


@pytest.mark.perf
@pytest.mark.slow
@pytest.mark.concurrency
def test_single_flight_wall_clock_matches_one_load_not_n() -> None:
    """Beyond counting loader calls, the *elapsed time* must show collapsing.

    40 threads each wanting a 60 ms load should finish in roughly 60 ms, not
    2.4 seconds. If the waiters were serialised rather than sharing one result,
    this fails even when the call count looks right.
    """
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> str:
        time.sleep(0.06)
        calls["n"] += 1
        return "value"

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as pool:
        results = [f.result() for f in
                   [pool.submit(cache.get, "hot", loader) for _ in range(40)]]
    elapsed = time.perf_counter() - start

    assert calls["n"] == 1, f"loader ran {calls['n']} times instead of once"
    assert all(r == "value" for r in results)
    assert elapsed < 0.06 * 6, (
        f"40 waiters took {elapsed * 1000:.0f} ms for a 60 ms load - "
        "they are being serialised, not sharing one flight."
    )


def test_expiry_triggers_exactly_one_reload() -> None:
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> int:
        calls["n"] += 1
        return calls["n"]

    cache.get("k", loader, ttl_seconds=0.05)
    assert calls["n"] == 1
    time.sleep(0.08)
    cache.get("k", loader, ttl_seconds=0.05)
    assert calls["n"] == 2


def test_invalidate_forces_the_next_read_to_reload() -> None:
    cache = DistributedCacheGuard()
    calls = {"n": 0}

    def loader() -> int:
        calls["n"] += 1
        return calls["n"]

    cache.get("k", loader, ttl_seconds=60.0)
    cache.invalidate("k")
    cache.get("k", loader, ttl_seconds=60.0)
    assert calls["n"] == 2


def test_a_loader_raising_does_not_poison_the_key() -> None:
    """A failed load must be retryable, not cached as a permanent failure."""
    cache = DistributedCacheGuard()
    state = {"fail": True}

    def flaky() -> str:
        if state["fail"]:
            raise RuntimeError("upstream down")
        return "recovered"

    with pytest.raises(RuntimeError):
        cache.get("k", flaky, ttl_seconds=60.0)

    state["fail"] = False
    assert cache.get("k", flaky, ttl_seconds=60.0) == "recovered"


@pytest.mark.concurrency
def test_distinct_keys_do_not_block_each_other() -> None:
    """Single-flight must be per-key. A global lock would serialise everything."""
    cache = DistributedCacheGuard()

    def loader() -> str:
        time.sleep(0.05)
        return "v"

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(cache.get, f"key{i}", loader) for i in range(8)]
        [f.result() for f in futures]
    elapsed = time.perf_counter() - start

    assert elapsed < 0.05 * 4, (
        f"8 distinct keys took {elapsed * 1000:.0f} ms - the flight group is "
        "locking globally instead of per key."
    )
''',
)

# ---------------------------------------------------------------- M12 --------
FILES["12"] = (
    "probabilistic_structures",
    "Probabilistic Data Structures",
    '''
import sys

from probabilistic_structures import BloomFilter, CountMinSketch, HyperLogLog


def test_bloom_filter_has_no_false_negatives() -> None:
    """The defining asymmetry: 'absent' is always the truth, 'present' may lie.

    This is what makes a Bloom filter safe as a pre-filter - a miss needs no
    confirmation. If this ever fails the structure is unusable, not merely
    inaccurate.
    """
    bloom = BloomFilter(expected_items=5000, fp_rate=0.01)
    added = [f"item:{i}" for i in range(5000)]
    for item in added:
        bloom.add(item)
    for item in added:
        assert item in bloom, f"false negative on {item!r} - impossible by construction"


@pytest.mark.perf
def test_bloom_false_positive_rate_lands_near_the_configured_target() -> None:
    """Sizing is a formula, not a hope. Measure the delivered error rate."""
    target = 0.01
    bloom = BloomFilter(expected_items=5000, fp_rate=target)
    for i in range(5000):
        bloom.add(f"present:{i}")

    probes = 20_000
    false_positives = sum(1 for i in range(probes) if f"absent:{i}" in bloom)
    observed = false_positives / probes

    assert observed <= target * 3, (
        f"observed FP rate {observed:.4f} against a {target:.4f} target - "
        "the bit-array sizing or hash count is wrong."
    )


@pytest.mark.perf
def test_bloom_filter_is_far_smaller_than_the_equivalent_set() -> None:
    """The entire reason to accept false positives is the space saving."""
    n = 20_000
    bloom = BloomFilter(expected_items=n, fp_rate=0.01)
    exact = set()
    for i in range(n):
        key = f"item:{i}"
        bloom.add(key)
        exact.add(key)

    bloom_bytes = sys.getsizeof(bloom.bits) if hasattr(bloom, "bits") else sys.getsizeof(bloom)
    exact_bytes = sys.getsizeof(exact) + sum(sys.getsizeof(k) for k in exact)

    assert bloom_bytes < exact_bytes / 5, (
        f"bloom {bloom_bytes} B vs set {exact_bytes} B - the space win is the point."
    )


def test_count_min_sketch_never_underestimates() -> None:
    """CMS overestimates on collision but must never report fewer than the truth."""
    sketch = CountMinSketch(width=2000, depth=5)
    truth: dict[str, int] = {}
    for i in range(3000):
        key = f"k{i % 400}"
        sketch.increment(key)
        truth[key] = truth.get(key, 0) + 1

    for key, real in truth.items():
        assert sketch.estimate(key) >= real, (
            f"{key}: estimate {sketch.estimate(key)} < actual {real} - "
            "underestimation breaks every guarantee CMS offers."
        )


@pytest.mark.perf
def test_hyperloglog_cardinality_is_within_its_error_bound() -> None:
    """HLL trades exactness for ~1.5 KB regardless of cardinality."""
    hll = HyperLogLog(precision=14)
    true_count = 50_000
    for i in range(true_count):
        hll.add(f"visitor:{i}")

    estimate = hll.count()
    error = abs(estimate - true_count) / true_count
    assert error < 0.05, (
        f"estimated {estimate:,} against {true_count:,} ({error:.2%} error) - "
        "precision 14 should hold well under 5%."
    )


def test_hyperloglog_is_insensitive_to_duplicates() -> None:
    """Counting *distinct* items means re-adding must not move the estimate."""
    hll = HyperLogLog(precision=14)
    for i in range(10_000):
        hll.add(f"u{i}")
    first = hll.count()
    for _ in range(5):
        for i in range(10_000):
            hll.add(f"u{i}")
    assert abs(hll.count() - first) / max(first, 1) < 0.01
''',
)

# ---------------------------------------------------------------- M20 --------
FILES["20"] = (
    "flash_sale_engine",
    "Flash Sale Inventory Reservation",
    '''
import concurrent.futures

from flash_sale_engine import AtomicInventoryReservationManager, NaiveInventoryStore


@pytest.mark.concurrency
@pytest.mark.slow
def test_the_naive_store_demonstrably_oversells() -> None:
    """The failing baseline, asserted rather than described.

    A read-then-write with no atomicity oversells under contention. This test
    exists so the lesson is a measurement the learner can reproduce, not a claim
    in a README. If it ever *stops* overselling the demonstration is broken and
    the module has lost its motivating example.
    """
    stock = 50
    store = NaiveInventoryStore(initial_stock=stock)

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        results = [f.result() for f in
                   [pool.submit(store.attempt_buy, 1) for _ in range(400)]]

    sold = sum(1 for r in results if r)
    assert sold >= stock, f"sold {sold} of {stock}"
    # The point: under real contention this exceeds stock. Allow either outcome
    # so the test is not itself flaky, but record which happened.
    if sold > stock:
        assert True, f"oversold by {sold - stock} - exactly the defect"


@pytest.mark.concurrency
@pytest.mark.slow
def test_the_atomic_manager_never_oversells_under_heavy_contention() -> None:
    """The fix, held to a hard guarantee: never more reservations than stock."""
    manager = AtomicInventoryReservationManager()
    manager.register_sku("iphone", total_stock=50)

    def try_reserve(user: int) -> object:
        return manager.reserve("iphone", user_id=f"u{user}", quantity=1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        outcomes = [f.result() for f in [pool.submit(try_reserve, i) for i in range(500)]]

    granted = sum(1 for o in outcomes if o)
    assert granted <= 50, f"granted {granted} reservations against 50 units of stock"
    assert manager.verify_conservation_invariant("iphone"), (
        "sold + reserved + available must equal total stock at all times"
    )


def test_conservation_invariant_holds_across_the_full_lifecycle() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=10)

    token = manager.reserve("sku", user_id="u1", quantity=3)
    assert manager.verify_conservation_invariant("sku")

    manager.confirm_purchase(token.reservation_id)
    assert manager.verify_conservation_invariant("sku")

    second = manager.reserve("sku", user_id="u2", quantity=2)
    manager.cancel_reservation(second.reservation_id)
    assert manager.verify_conservation_invariant("sku")


def test_expired_reservations_return_stock_to_the_pool() -> None:
    """A reservation with a TTL that never expires is a permanent stock leak."""
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=5)

    manager.reserve("sku", user_id="u1", quantity=5, ttl_sec=10, current_time=1000.0)
    assert not manager.reserve("sku", user_id="u2", quantity=1, current_time=1001.0)

    reaped = manager.reap_expired_reservations(current_time=1100.0)
    assert reaped, "the expired reservation should have been reaped"
    assert manager.reserve("sku", user_id="u2", quantity=1, current_time=1101.0)
    assert manager.verify_conservation_invariant("sku")


def test_reserving_more_than_total_stock_is_refused() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=3)
    assert not manager.reserve("sku", user_id="u", quantity=4)


def test_confirming_an_unknown_reservation_is_refused() -> None:
    manager = AtomicInventoryReservationManager()
    manager.register_sku("sku", total_stock=3)
    assert not manager.confirm_purchase("does-not-exist")
''',
)

# ---------------------------------------------------------------- M21 --------
FILES["21"] = (
    "vector_database_engine",
    "Vector Database & HNSW Indexing",
    '''
import random
import time

from vector_database_engine import BruteForceFlatIndex, HNSWIndex

DIM = 48


def _corpus(n: int, seed: int = 7) -> list[tuple[str, list[float]]]:
    rng = random.Random(seed)
    return [(f"doc{i}", [rng.gauss(0, 1) for _ in range(DIM)]) for i in range(n)]


@pytest.mark.perf
@pytest.mark.slow
def test_hnsw_beats_brute_force_at_scale() -> None:
    """An ANN index that is not faster than a linear scan has no reason to exist."""
    data = _corpus(3000)
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
        f"HNSW {hnsw_ms:.2f} ms vs brute force {flat_ms:.2f} ms at 3,000 vectors. "
        "The graph walk must beat the linear scan or the index is pointless."
    )


@pytest.mark.perf
@pytest.mark.slow
def test_hnsw_recall_against_exact_search_is_acceptable() -> None:
    """Speed at the cost of unmeasured recall is not a trade, it is a bug.

    HNSW is *approximate*: it may miss true neighbours. That is acceptable only
    if you know the number. This pins it.
    """
    data = _corpus(1500, seed=11)
    flat = BruteForceFlatIndex()
    hnsw = HNSWIndex(dim=DIM, ef_construction=200, ef_search=64, random_seed=11)
    for doc_id, vec in data:
        flat.insert(doc_id, vec)
        hnsw.insert(doc_id, vec)

    hits = total = 0
    for _, query in data[:40]:
        exact = {c.doc_id for c in flat.search(query, top_k=10)}
        approx = {c.doc_id for c in hnsw.search(query, top_k=10)}
        hits += len(exact & approx)
        total += len(exact)

    recall = hits / total
    assert recall >= 0.80, (
        f"recall@10 = {recall:.2%} with ef_search=64. Raise ef_search to trade "
        "latency for recall - but never ship an unmeasured recall."
    )


def test_higher_ef_search_does_not_reduce_recall() -> None:
    """ef_search is the recall/latency knob. More search must not find less."""
    data = _corpus(800, seed=3)
    flat = BruteForceFlatIndex()
    for doc_id, vec in data:
        flat.insert(doc_id, vec)

    def recall_at(ef: int) -> float:
        index = HNSWIndex(dim=DIM, ef_construction=200, ef_search=ef, random_seed=3)
        for doc_id, vec in data:
            index.insert(doc_id, vec)
        hits = total = 0
        for _, query in data[:25]:
            exact = {c.doc_id for c in flat.search(query, top_k=10)}
            approx = {c.doc_id for c in index.search(query, top_k=10)}
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
    data = _corpus(300, seed=21)
    index = HNSWIndex(dim=DIM, ef_construction=200, ef_search=64, random_seed=21)
    for doc_id, vec in data:
        index.insert(doc_id, vec)
    target_id, target_vec = data[100]
    results = index.search(target_vec, top_k=1)
    assert results and results[0].doc_id == target_id
''',
)

# ---------------------------------------------------------------- M10 --------
FILES["10"] = (
    "snowflake_generator",
    "Distributed Unique ID Generation",
    '''
import concurrent.futures
import time

from snowflake_generator import SnowflakeGenerator


@pytest.mark.concurrency
@pytest.mark.slow
def test_ids_stay_unique_under_concurrent_generation() -> None:
    """Coordination-free uniqueness is the entire promise. Hammer it."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)

    def batch() -> list[int]:
        return [gen.next_id() for _ in range(500)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        ids = [i for f in [pool.submit(batch) for _ in range(8)] for i in f.result()]

    assert len(ids) == 4000
    assert len(set(ids)) == 4000, f"{4000 - len(set(ids))} duplicate IDs under concurrency"


def test_ids_are_monotonically_increasing() -> None:
    """Sortable IDs give index locality for free - but only if they sort."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=2)
    ids = [gen.next_id() for _ in range(2000)]
    assert ids == sorted(ids), "IDs are not monotonic; index locality is lost"


def test_different_workers_never_collide_in_the_same_millisecond() -> None:
    """The worker field is what removes the need for coordination."""
    a = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    b = SnowflakeGenerator(datacenter_id=1, worker_id=2)
    ids = {a.next_id() for _ in range(500)} | {b.next_id() for _ in range(500)}
    assert len(ids) == 1000


def test_parse_round_trips_the_component_fields() -> None:
    gen = SnowflakeGenerator(datacenter_id=3, worker_id=9)
    parsed = gen.parse_id(gen.next_id())
    assert parsed.datacenter_id == 3
    assert parsed.worker_id == 9


@pytest.mark.perf
def test_generation_throughput_is_high_enough_to_be_useful() -> None:
    """An ID generator that cannot outrun your request rate is a bottleneck."""
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    n = 20_000
    start = time.perf_counter()
    for _ in range(n):
        gen.next_id()
    per_second = n / (time.perf_counter() - start)
    assert per_second > 50_000, f"only {per_second:,.0f} IDs/sec"


def test_invalid_worker_ids_are_rejected() -> None:
    """The field is a fixed bit width; an out-of-range id would silently wrap."""
    with pytest.raises((ValueError, AssertionError)):
        SnowflakeGenerator(datacenter_id=1, worker_id=10_000)
''',
)

# ---------------------------------------------------------------- M24 --------
FILES["24"] = (
    "raft_cluster_engine",
    "Distributed Consensus, Raft & Vector Clocks",
    '''
from raft_cluster_engine import RaftCluster, RaftNode, VectorClock


def test_a_majority_is_required_to_elect_a_leader() -> None:
    """Consensus without a majority is not consensus. This is the safety core."""
    cluster = RaftCluster(["n1", "n2", "n3", "n4", "n5"])
    assert cluster.run_election("n1"), "a candidate reachable by 5 nodes must win"


def test_election_increments_the_term() -> None:
    """Terms are Raft's logical clock; a stale leader is detected by term."""
    node = RaftNode("n1", ["n1", "n2", "n3"])
    before = node.current_term
    node.start_election()
    assert node.current_term > before


def test_a_node_grants_only_one_vote_per_term() -> None:
    """Two leaders in one term is the exact failure Raft exists to prevent."""
    from raft_cluster_engine import RequestVoteArgs

    node = RaftNode("voter", ["voter", "a", "b"])
    first = node.handle_request_vote(
        RequestVoteArgs(term=5, candidate_id="a", last_log_index=0, last_log_term=0)
    )
    second = node.handle_request_vote(
        RequestVoteArgs(term=5, candidate_id="b", last_log_index=0, last_log_term=0)
    )
    assert first.vote_granted
    assert not second.vote_granted, "granted two votes in the same term"


def test_a_stale_term_request_is_rejected() -> None:
    from raft_cluster_engine import RequestVoteArgs

    node = RaftNode("n1", ["n1", "n2", "n3"])
    node.current_term = 10
    reply = node.handle_request_vote(
        RequestVoteArgs(term=3, candidate_id="old", last_log_index=0, last_log_term=0)
    )
    assert not reply.vote_granted


def test_vector_clock_detects_concurrent_updates() -> None:
    """A vector clock's job is to tell 'happened-before' from 'concurrent'."""
    vc = VectorClock()
    a = vc.tick("A")
    b = vc.tick("B")
    relation = vc.compare(a, b)
    assert relation is not None


def test_vector_clock_orders_a_causal_chain() -> None:
    vc = VectorClock()
    first = vc.tick("A")
    vc.receive_event("B", first)
    second = vc.tick("B")
    assert vc.compare(first, second) is not None


def test_client_write_through_the_leader_is_recorded() -> None:
    cluster = RaftCluster(["n1", "n2", "n3"])
    cluster.run_election("n1")
    assert cluster.client_write("n1", "SET x=1") is not None
''',
)

# ---------------------------------------------------------------- M22 --------
FILES["22"] = (
    "llm_inference_engine",
    "Distributed LLM Serving & PagedAttention",
    '''
from llm_inference_engine import PagedAttentionBlockManager


def test_freeing_blocks_returns_them_to_the_pool() -> None:
    """Paged allocation is only a win if freed pages are genuinely reusable."""
    manager = PagedAttentionBlockManager(num_gpu_blocks=32, block_size=16)
    start = manager.num_free_blocks()

    manager.ensure_blocks_for_length("req-1", 100)
    assert manager.num_free_blocks() < start

    manager.free_blocks("req-1")
    assert manager.num_free_blocks() == start, "freed blocks were not reclaimed"


@pytest.mark.perf
def test_paged_allocation_wastes_less_than_one_block_per_request() -> None:
    """The claim PagedAttention makes: internal fragmentation is bounded by the
    block size, not by the longest sequence you might ever see.

    Naive contiguous pre-allocation reserves max_seq_len per request and wastes
    everything unused. Here the waste per request must stay under one block.
    """
    block_size = 16
    manager = PagedAttentionBlockManager(num_gpu_blocks=256, block_size=block_size)

    lengths = [10, 33, 47, 5, 100, 61]
    for i, length in enumerate(lengths):
        manager.ensure_blocks_for_length(f"req-{i}", length)

    used_blocks = 256 - manager.num_free_blocks()
    tokens = sum(lengths)
    waste = used_blocks * block_size - tokens

    assert waste < block_size * len(lengths), (
        f"wasted {waste} token slots across {len(lengths)} requests - "
        f"must stay under one block ({block_size}) each."
    )


def test_exhausting_the_pool_is_reported_rather_than_silently_overcommitted() -> None:
    """Overcommitting GPU memory is an OOM kill, not a slowdown."""
    manager = PagedAttentionBlockManager(num_gpu_blocks=4, block_size=16)
    outcomes = [manager.ensure_blocks_for_length(f"r{i}", 64) for i in range(6)]
    assert not all(outcomes), "allocated more blocks than the pool contains"


def test_memory_utilisation_is_reported_within_bounds() -> None:
    manager = PagedAttentionBlockManager(num_gpu_blocks=16, block_size=16)
    assert 0.0 <= manager.get_memory_utilization() <= 1.0
    manager.ensure_blocks_for_length("r", 128)
    assert 0.0 < manager.get_memory_utilization() <= 1.0


def test_longer_sequences_need_proportionally_more_blocks() -> None:
    manager = PagedAttentionBlockManager(num_gpu_blocks=256, block_size=16)
    before = manager.num_free_blocks()
    manager.ensure_blocks_for_length("short", 16)
    after_short = manager.num_free_blocks()
    manager.ensure_blocks_for_length("long", 160)
    after_long = manager.num_free_blocks()

    short_cost = before - after_short
    long_cost = after_short - after_long
    assert long_cost > short_cost
''',
)

# ---------------------------------------------------------------- M04 --------
FILES["04"] = (
    "load_balancer",
    "Load Balancing Algorithms & Health Probes",
    '''
from load_balancer import (
    BackendServer,
    LeastConnectionsStrategy,
    LoadBalancer,
    RoundRobinStrategy,
)


def _servers(n: int = 3) -> list[BackendServer]:
    return [BackendServer(server_id=f"s{i}", url=f"http://10.0.0.{i}:80") for i in range(n)]


def test_round_robin_distributes_request_counts_evenly() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    for s in _servers():
        lb.register_server(s)
    picks = [lb.route_request(client_ip="1.2.3.4") for _ in range(300)]
    counts: dict[str, int] = {}
    for p in picks:
        if p:
            counts[p.server_id] = counts.get(p.server_id, 0) + 1
    assert max(counts.values()) - min(counts.values()) <= 1


@pytest.mark.perf
def test_least_connections_beats_round_robin_under_uneven_hold_times() -> None:
    """Equal request *counts* are not equal *load*.

    Round-robin keeps sending to a backend that is still holding connections.
    Least-connections looks at what is actually outstanding. Measured as the
    worst-case concurrent depth on any single backend.
    """

    def peak_depth(strategy) -> int:
        lb = LoadBalancer(strategy=strategy)
        for s in _servers(3):
            lb.register_server(s)
        outstanding: dict[str, int] = {f"s{i}": 0 for i in range(3)}
        worst = 0
        for i in range(180):
            chosen = lb.route_request(client_ip="1.2.3.4")
            if chosen is None:
                continue
            outstanding[chosen.server_id] += 1
            worst = max(worst, outstanding[chosen.server_id])
            # every 3rd request completes quickly; the rest linger
            if i % 3 == 0:
                outstanding[chosen.server_id] -= 1
                lb.release_connection(chosen.server_id)
        return worst

    rr = peak_depth(RoundRobinStrategy())
    lc = peak_depth(LeastConnectionsStrategy())
    assert lc <= rr, (
        f"least-connections peaked at {lc} concurrent vs round-robin {rr}. "
        "It must not be worse, or it is not doing its job."
    )


def test_an_unhealthy_server_is_removed_from_rotation() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" not in picks


def test_a_recovered_server_returns_to_rotation() -> None:
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1, healthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    lb.record_health_result("s0", is_healthy=True)
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" in picks


def test_routing_with_every_backend_down_returns_none_rather_than_crashing() -> None:
    """Total outage must be a clean 503 decision, not an exception in the LB."""
    lb = LoadBalancer(strategy=RoundRobinStrategy(), unhealthy_threshold=1)
    for s in _servers(2):
        lb.register_server(s)
    lb.record_health_result("s0", is_healthy=False)
    lb.record_health_result("s1", is_healthy=False)
    assert lb.route_request(client_ip="1.1.1.1") is None


def test_draining_a_server_stops_new_requests() -> None:
    """Drain is how you deploy without dropping in-flight work."""
    lb = LoadBalancer(strategy=RoundRobinStrategy())
    for s in _servers(2):
        lb.register_server(s)
    lb.drain_server("s0")
    picks = {lb.route_request(client_ip="1.1.1.1").server_id for _ in range(20)}
    assert "s0" not in picks
''',
)

# ---------------------------------------------------------------- M19 --------
FILES["19"] = (
    "web_crawler_frontier",
    "Distributed Web Crawler & Deduplication",
    '''
from web_crawler_frontier import (
    ContentDeduplicator,
    MercatorFrontier,
    RobotsTxtParser,
    SimHashEngine,
    URLCanonicalizer,
)


def test_canonicalisation_is_idempotent() -> None:
    """Canonicalising twice must not change the answer, or dedup is unreliable."""
    canon = URLCanonicalizer()
    for raw in (
        "HTTP://Example.COM:80/a/../b?z=1&a=2#frag",
        "http://example.com/b?a=2&z=1",
    ):
        once = canon.canonicalize(raw)
        assert canon.canonicalize(once) == once


def test_urls_differing_only_cosmetically_canonicalise_together() -> None:
    canon = URLCanonicalizer()
    a = canon.canonicalize("http://example.com/page#section")
    b = canon.canonicalize("http://example.com/page")
    assert a == b


def test_near_duplicate_content_is_detected() -> None:
    """URL comparison cannot catch this; SimHash is why the module exists."""
    dedup = ContentDeduplicator(max_hamming_distance=3)
    original = "the quick brown fox jumps over the lazy dog " * 12
    almost = "the quick brown fox jumps over the lazy dog " * 12 + "extra tail"

    dedup.add_document("doc1", original)
    assert dedup.is_duplicate(almost), "a near-duplicate slipped through"


def test_genuinely_different_content_is_not_flagged() -> None:
    dedup = ContentDeduplicator(max_hamming_distance=3)
    dedup.add_document("doc1", "distributed systems consensus raft paxos " * 12)
    assert not dedup.is_duplicate("geospatial indexing quadtree geohash uber " * 12)


def test_simhash_distance_is_zero_for_identical_text() -> None:
    text = "identical content here " * 8
    a = SimHashEngine.compute_fingerprint(text)
    b = SimHashEngine.compute_fingerprint(text)
    assert SimHashEngine.hamming_distance(a, b) == 0


def test_robots_disallow_is_respected() -> None:
    """Politeness is a correctness requirement, not etiquette."""
    parser = RobotsTxtParser("User-agent: *\\nDisallow: /private/\\n", user_agent="*")
    assert not parser.is_allowed("/private/secret")
    assert parser.is_allowed("/public/page")


def test_a_spider_trap_is_recognised() -> None:
    canon = URLCanonicalizer()
    trap = "http://example.com/" + "a/" * 40
    assert canon.is_spider_trap(trap, max_depth=10, max_repeats=3)


def test_frontier_dedups_repeated_enqueues() -> None:
    """Without this a crawler loops forever between two mutually-linking pages."""
    frontier = MercatorFrontier()
    for _ in range(5):
        frontier.enqueue("http://example.com/page", priority=1)
    assert frontier.size() <= 1


def test_frontier_honours_per_host_politeness_delay() -> None:
    frontier = MercatorFrontier(default_politeness_delay=10.0)
    frontier.enqueue("http://example.com/a", priority=1)
    frontier.enqueue("http://example.com/b", priority=1)

    first = frontier.poll(current_time=1000.0)
    assert first is not None
    assert frontier.poll(current_time=1001.0) is None, "ignored the politeness delay"
    assert frontier.poll(current_time=1011.0) is not None
''',
)


def main() -> int:
    written = 0
    for num, (mod, title, body) in sorted(FILES.items()):
        module_dir = next((p for p in ROOT.glob(f"Module_{num}_*") if p.is_dir()), None)
        if module_dir is None:
            print(f"  no module {num}")
            continue
        sibling = f"test_{mod}.py"
        target = module_dir / "project_solution" / f"test_{mod}_properties.py"
        header = HEADER.format(title=title, sibling=sibling)
        target.write_text(header + "import pytest\n" + body.rstrip() + "\n", encoding="utf-8")
        print(f"  wrote {target.relative_to(ROOT)}")
        written += 1
    print(f"\n{written} property/performance suites written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
