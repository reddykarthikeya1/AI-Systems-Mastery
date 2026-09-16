"""Problem-bank suite for Module_15_Systems_Level_Structures_SkipLists_BloomFilters_LRU.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_lru_cache import simulate_lru
from p02_bloom_filter import bloom_check
from p03_skip_list import simulate_skip_list
from p04_ring_buffer import simulate_ring_buffer
from p05_lfu_cache import simulate_lfu
from p06_hyperloglog import approx_distinct
from p07_count_min_sketch import count_min_estimate
from p08_consistent_hash_ring import remap_fraction


def test_p01_lru_cache():
    """LRU Cache With O(1) Operations — Hash map + doubly linked list (Hard)."""
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3), ("get", 2, 0)]
    assert simulate_lru(2, ops) == [1, -1]
    # A miss on an empty cache.
    assert simulate_lru(1, [("get", 1, 0)]) == [-1]
    # Updating a key must not evict anything.
    ops = [("put", 1, 1), ("put", 1, 2), ("get", 1, 0)]
    assert simulate_lru(1, ops) == [2]
    # A get counts as a use, protecting the key from eviction.
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3),
           ("get", 1, 0), ("get", 2, 0), ("get", 3, 0)]
    assert simulate_lru(2, ops) == [1, 1, -1, 3]
    # A put also counts as a use.
    ops = [("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3),
           ("get", 2, 0), ("get", 1, 0)]
    assert simulate_lru(2, ops) == [-1, 10]
    # Capacity 1 evicts on every new key.
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("get", 2, 0)]
    assert simulate_lru(1, ops) == [-1, 2]
    with pytest.raises(ValueError):
        simulate_lru(0, [("get", 1, 0)])
    # Cross-check against a naive list-based model.
    import random
    random.seed(21)
    cap = 4
    order: list[int] = []
    model: dict[int, int] = {}
    seq, expected = [], []
    for _ in range(2000):
        k = random.randint(1, 8)
        if random.random() < 0.5:
            v = random.randint(0, 100)
            seq.append(('put', k, v))
            if k in model:
                order.remove(k)
            model[k] = v
            order.append(k)
            if len(order) > cap:
                del model[order.pop(0)]
        else:
            seq.append(('get', k, 0))
            if k in model:
                order.remove(k)
                order.append(k)
                expected.append(model[k])
            else:
                expected.append(-1)
    assert simulate_lru(cap, seq) == expected

def test_p02_bloom_filter():
    """Bloom Filter: No False Negatives — Bloom filter (Hard)."""
    # The core guarantee: no false negatives, ever.
    words = ["cat", "dog", "bird", "fish", "horse", "mouse"]
    verdicts = bloom_check(words, words)
    assert all(verdicts), "an inserted item must never report absent"
    # Empty filter: nothing can be present.
    assert bloom_check([], ["anything"]) == [False]
    assert bloom_check([], []) == []
    # Deterministic across calls.
    a = bloom_check(["x", "y"], ["x", "z", "y", "w"])
    b = bloom_check(["x", "y"], ["x", "z", "y", "w"])
    assert a == b, "the filter must be reproducible"
    # With a generous bit budget, false positives should be rare.
    inserted = [f"item-{i}" for i in range(200)]
    absent = [f"missing-{i}" for i in range(2000)]
    fp = sum(bloom_check(inserted, absent, bits=65536, hashes=4))
    assert fp < 100, f"false positive rate looks too high: {fp}/2000"
    # And the guarantee still holds at that scale.
    assert all(bloom_check(inserted, inserted, bits=65536, hashes=4))
    # A tiny filter produces many false positives - which is allowed,, # and is exactly the trade being made.
    assert all(bloom_check(inserted, inserted, bits=64, hashes=3))
    with pytest.raises(ValueError):
        bloom_check(["a"], ["a"], bits=0)

def test_p03_skip_list():
    """Skip List: Insert, Search, Delete — Skip list (Hard)."""
    ops = [("insert", 3), ("insert", 1), ("search", 3), ("items", 0),
           ("delete", 3), ("search", 3)]
    assert simulate_skip_list(ops) == [True, [1, 3], True, False]
    # Searching an empty structure.
    assert simulate_skip_list([("search", 1), ("items", 0)]) == [False, []]
    # Inserts are idempotent.
    ops = [("insert", 5), ("insert", 5), ("items", 0)]
    assert simulate_skip_list(ops) == [[5]]
    # Deleting something absent returns False.
    assert simulate_skip_list([("delete", 9)]) == [False]
    # Contents stay sorted regardless of insertion order.
    ops = [("insert", v) for v in (5, 1, 9, 3, 7)] + [("items", 0)]
    assert simulate_skip_list(ops) == [[1, 3, 5, 7, 9]]
    # Negative values.
    ops = [("insert", -3), ("insert", 0), ("insert", -7), ("items", 0)]
    assert simulate_skip_list(ops) == [[-7, -3, 0]]
    with pytest.raises(ValueError):
        simulate_skip_list([("frobnicate", 1)])
    # Cross-check against a plain sorted set over a long sequence.
    import random as _r
    _r.seed(31)
    model: set[int] = set()
    seq, expected = [], []
    for _ in range(1500):
        v = _r.randint(1, 60)
        r = _r.random()
        if r < 0.45:
            seq.append(('insert', v))
            model.add(v)
        elif r < 0.7:
            seq.append(('search', v))
            expected.append(v in model)
        elif r < 0.9:
            seq.append(('delete', v))
            expected.append(v in model)
            model.discard(v)
        else:
            seq.append(('items', 0))
            expected.append(sorted(model))
    assert simulate_skip_list(seq) == expected

def test_p04_ring_buffer():
    """Fixed-Capacity Ring Buffer — Circular buffer (Medium)."""
    ops = [("push", 1), ("push", 2), ("push", 3), ("push", 4), ("items", 0)]
    assert simulate_ring_buffer(3, ops) == [[2, 3, 4]]
    # Popping an empty buffer.
    assert simulate_ring_buffer(2, [("pop", 0)]) == [None]
    # FIFO order.
    ops = [("push", 1), ("push", 2), ("pop", 0), ("pop", 0), ("pop", 0)]
    assert simulate_ring_buffer(2, ops) == [1, 2, None]
    # Wrapping around after pops.
    ops = [("push", 1), ("push", 2), ("pop", 0), ("push", 3), ("items", 0)]
    assert simulate_ring_buffer(2, ops) == [1, [2, 3]]
    # Capacity 1 overwrites on every push.
    ops = [("push", 1), ("push", 2), ("items", 0), ("pop", 0)]
    assert simulate_ring_buffer(1, ops) == [[2], 2]
    # Overwriting many times over.
    ops = [("push", v) for v in range(10)] + [("items", 0)]
    assert simulate_ring_buffer(3, ops) == [[7, 8, 9]]
    with pytest.raises(ValueError):
        simulate_ring_buffer(0, [("pop", 0)])
    # Cross-check against a deque with maxlen, which has the same, # overwrite-oldest semantics.
    import random
    from collections import deque
    random.seed(41)
    cap = 5
    model: deque[int] = deque(maxlen=cap)
    seq, expected = [], []
    for _ in range(1200):
        r = random.random()
        if r < 0.55:
            v = random.randint(0, 99)
            seq.append(('push', v))
            model.append(v)
        elif r < 0.85:
            seq.append(('pop', 0))
            expected.append(model.popleft() if model else None)
        else:
            seq.append(('items', 0))
            expected.append(list(model))
    assert simulate_ring_buffer(cap, seq) == expected

def test_p05_lfu_cache():
    """LFU Cache — Frequency buckets (Hard)."""
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3),
           ("get", 2, 0), ("get", 3, 0)]
    assert simulate_lfu(2, ops) == [1, -1, 3]
    # A miss on an empty cache.
    assert simulate_lfu(1, [("get", 1, 0)]) == [-1]
    # Frequency beats recency: key 1 is used twice, so key 2 goes.
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("get", 1, 0),
           ("put", 3, 3), ("get", 2, 0), ("get", 1, 0)]
    assert simulate_lfu(2, ops) == [1, 1, -1, 1]
    # Ties broken by least-recently-used.
    ops = [("put", 1, 1), ("put", 2, 2), ("put", 3, 3), ("get", 1, 0), ("get", 2, 0)]
    assert simulate_lfu(2, ops) == [-1, 2]
    # An update counts as a use.
    ops = [("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3),
           ("get", 2, 0), ("get", 1, 0)]
    assert simulate_lfu(2, ops) == [-1, 10]
    # Capacity 1.
    ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("get", 2, 0)]
    assert simulate_lfu(1, ops) == [-1, 2]
    with pytest.raises(ValueError):
        simulate_lfu(0, [("get", 1, 0)])

def test_p06_hyperloglog():
    """Approximate Distinct Count — Probabilistic cardinality estimation (Hard)."""
    # Exactness is not the contract, the error bound is.
    assert approx_distinct([]) == 0
    # Small cardinalities: the linear-counting correction makes these, # close to exact.
    for true_count in (1, 2, 5, 10, 50):
        items = [f'v{i}' for i in range(true_count)]
        got = approx_distinct(items)
        assert abs(got - true_count) <= max(2, true_count * 0.2), (true_count, got)
    # Duplicates must not inflate the estimate.
    assert approx_distinct(['a'] * 1000 + ['b'] * 1000) <= 4
    # The headline accuracy claim, at three scales.
    for true_count in (1000, 10_000, 50_000):
        items = [f'user-{i}' for i in range(true_count)]
        got = approx_distinct(items, registers=1024)
        error = abs(got - true_count) / true_count
        assert error < 0.15, f'{true_count}: estimated {got}, error {error:.1%}'
    # Deterministic.
    data = [f'x{i}' for i in range(5000)]
    assert approx_distinct(data) == approx_distinct(data)
    # Order must not matter.
    import random
    shuffled = data[:]
    random.Random(7).shuffle(shuffled)
    assert approx_distinct(data) == approx_distinct(shuffled)
    with pytest.raises(ValueError):
        approx_distinct(['a'], registers=100)
    with pytest.raises(ValueError):
        approx_distinct(['a'], registers=8)

def test_p07_count_min_sketch():
    """Count-Min Sketch: Frequency Estimation — Count-Min sketch (Hard)."""
    # The one-sided guarantee: never an underestimate.
    from collections import Counter
    items = ['a'] * 5 + ['b'] * 3 + ['c']
    truth = Counter(items)
    queries = ['a', 'b', 'c', 'zzz']
    got = count_min_estimate(items, queries)
    for q, estimate in zip(queries, got):
        assert estimate >= truth[q], (q, estimate, truth[q])
    # With a generous table, the estimates should be exact here.
    assert count_min_estimate(items, ['a', 'b', 'c']) == [5, 3, 1]
    # An empty stream.
    assert count_min_estimate([], ['a']) == [0]
    assert count_min_estimate([], []) == []
    # Deterministic.
    data = [f'k{i % 500}' for i in range(20_000)]
    assert count_min_estimate(data, ['k1']) == count_min_estimate(data, ['k1'])
    # At scale, the guarantee still holds and the error stays small.
    truth = Counter(data)
    keys = [f'k{i}' for i in range(500)]
    estimates = count_min_estimate(data, keys, width=4096, depth=5)
    for k, e in zip(keys, estimates):
        assert e >= truth[k], (k, e, truth[k])
    assert sum(e - truth[k] for k, e in zip(keys, estimates)) <= len(keys) * 5
    # A tiny table overestimates - allowed, and the point of the trade.
    tiny = count_min_estimate(data, ['k1'], width=4, depth=1)
    assert tiny[0] >= truth['k1']
    with pytest.raises(ValueError):
        count_min_estimate(['a'], ['a'], width=0)

def test_p08_consistent_hash_ring():
    """Consistent Hashing Ring — Consistent hashing (Hard)."""
    nodes = ['node-a', 'node-b', 'node-c']
    keys = [f'key-{i}' for i in range(10_000)]
    fraction = remap_fraction(nodes, 'node-d', keys)
    # The headline property: about 1/(n+1) of keys move, NOT most of them.
    assert 0.15 < fraction < 0.35, f'expected ~0.25, got {fraction:.3f}'
    # Compare against naive modulo hashing, which remaps almost everything.
    import hashlib
    def _mod_owner(key, n):
        d = int.from_bytes(hashlib.md5(key.encode()).digest()[:8], 'big')
        return d % n
    naive_moved = sum(
        1 for k in keys if _mod_owner(k, 3) != _mod_owner(k, 4)
    ) / len(keys)
    assert naive_moved > 0.6, f'naive modulo should thrash, got {naive_moved:.3f}'
    assert fraction < naive_moved / 2
    # Deterministic.
    assert remap_fraction(nodes, 'node-d', keys) == fraction
    # A single starting node: adding a second moves about half.
    half = remap_fraction(['only'], 'second', keys)
    assert 0.35 < half < 0.65, half
    # More nodes means a smaller disruption.
    many = [f'n{i}' for i in range(10)]
    small = remap_fraction(many, 'n10', keys)
    assert small < fraction, (small, fraction)
    assert 0.03 < small < 0.20, small
    # Edge cases.
    assert remap_fraction(['a'], 'b', []) == 0.0
    with pytest.raises(ValueError):
        remap_fraction([], 'a', keys)
