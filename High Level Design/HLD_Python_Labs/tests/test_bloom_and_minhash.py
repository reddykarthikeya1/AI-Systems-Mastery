"""Tests for Bloom Filter vs. MinHash & LSH (Chapter 16)."""
import pytest
from ch16_bloom_filter.bloom_and_minhash import (
    BloomFilter,
    CountingBloomFilter,
    MinHash,
    LSHIndex,
    calculate_optimal_bloom_params,
)


def test_bloom_filter_zero_false_negatives():
    bf = BloomFilter.from_capacity(expected_items=1000, false_positive_rate=0.01)

    items = [f"item_{i}" for i in range(500)]
    for item in items:
        bf.add(item)

    # Core Invariant: Zero False Negatives
    for item in items:
        assert bf.contains(item) is True

    # Items definitely not added
    unseen = [f"nonexistent_{i}" for i in range(500)]
    false_positives = sum(1 for item in unseen if bf.contains(item))
    observed_fp_rate = false_positives / len(unseen)

    # False positive rate should be around 1% (<= 5% with statistical margin)
    assert observed_fp_rate <= 0.05


def test_optimal_bloom_params():
    m, k = calculate_optimal_bloom_params(n=10000, p=0.01)
    assert m > 0
    assert k > 0
    # For p=0.01, k is typically around 7
    assert 5 <= k <= 10

    with pytest.raises(ValueError):
        calculate_optimal_bloom_params(n=0, p=0.01)
    with pytest.raises(ValueError):
        calculate_optimal_bloom_params(n=100, p=1.5)


def test_counting_bloom_filter_add_and_remove():
    cbf = CountingBloomFilter.from_capacity(expected_items=100, false_positive_rate=0.01)

    # Add item
    cbf.add("user:alpha")
    assert cbf.contains("user:alpha") is True
    assert cbf.contains("user:beta") is False

    # Calling remove without verified_present raises TypeError (no default allowed)
    with pytest.raises(TypeError):
        cbf.remove("user:alpha")

    # Calling remove with verified_present=False raises ValueError
    with pytest.raises(ValueError) as excinfo:
        cbf.remove("user:alpha", verified_present=False)
    assert "requires explicit verified_present=True proof of prior insertion" in str(excinfo.value)

    # Legitimate removal with explicit verified_present=True
    cbf.remove("user:alpha", verified_present=True)
    assert cbf.contains("user:alpha") is False

    # Remove non-existent item with verified_present=True does not error
    cbf.remove("user:beta", verified_present=True)
    assert cbf.contains("user:beta") is False


def test_counting_bloom_filter_false_positive_removal_risk():
    """Demonstrate the False-Positive Removal Hazard in Counting Bloom Filters:

    1. Legitimate item A is inserted.
    2. Item B was NEVER inserted, but contains(Item B) returns True due to a false-positive hash collision.
    3. Calling remove() or remove_safe() without keyword arguments raises TypeError.
    4. Calling remove() or remove_safe() with verified_present=False raises ValueError.
    5. If a caller erroneously forces removal with verified_present=True (falsely assuming existence),
       decrementing shared counters corrupts the filter and creates a FALSE NEGATIVE for legitimate Item A!
    """
    cbf = CountingBloomFilter(size_m=16, hash_count_k=1)

    item_a = "legitimate_key"
    cbf.add(item_a)
    slot_a = cbf._get_hashes(item_a)[0]
    assert cbf.contains(item_a) is True

    # Find an uninserted item that collides on the same slot
    colliding_uninserted = None
    for i in range(1000):
        probe = f"unseen_key_{i}"
        if cbf._get_hashes(probe)[0] == slot_a:
            colliding_uninserted = probe
            break

    assert colliding_uninserted is not None
    # Probabilistic false positive: contains() returns True even though it was never added!
    assert cbf.contains(colliding_uninserted) is True

    # Omitting keyword argument raises TypeError
    with pytest.raises(TypeError):
        cbf.remove(colliding_uninserted)
    with pytest.raises(TypeError):
        cbf.remove_safe(colliding_uninserted)

    # remove and remove_safe with verified_present=False block the unverified removal
    with pytest.raises(ValueError) as excinfo:
        cbf.remove_safe(colliding_uninserted, verified_present=False)
    assert "requires explicit verified_present=True proof of prior insertion" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        cbf.remove(colliding_uninserted, verified_present=False)
    assert "requires explicit verified_present=True proof of prior insertion" in str(excinfo.value)

    # If mistakenly verified and removed:
    cbf.remove(colliding_uninserted, verified_present=True)

    # THE HAZARD DEMONSTRATED: Legitimate item_a now suffers a FALSE NEGATIVE!
    assert cbf.contains(item_a) is False


def test_counting_bloom_filter_duplicates():
    cbf = CountingBloomFilter.from_capacity(expected_items=50, false_positive_rate=0.01)

    # Add duplicate item twice
    cbf.add("order:101")
    cbf.add("order:101")
    assert cbf.contains("order:101") is True

    # First removal decrements counter, item still exists
    cbf.remove("order:101", verified_present=True)
    assert cbf.contains("order:101") is True

    # Second removal decrements counter to zero
    cbf.remove("order:101", verified_present=True)
    assert cbf.contains("order:101") is False


def test_minhash_jaccard_similarity():
    text1 = "distributed systems high level design microservices architecture event driven"
    text2 = "distributed systems high level design microservices architecture event driven"
    text3 = "completely unrelated cooking recipe with baking powder salt and eggs"

    shingles1 = MinHash.shingle_text(text1, n_gram=2)
    shingles2 = MinHash.shingle_text(text2, n_gram=2)
    shingles3 = MinHash.shingle_text(text3, n_gram=2)

    mh1 = MinHash(num_hashes=128, seed=42)
    mh1.update(shingles1)

    mh2 = MinHash(num_hashes=128, seed=42)
    mh2.update(shingles2)

    mh3 = MinHash(num_hashes=128, seed=42)
    mh3.update(shingles3)

    # Identical texts -> estimated similarity == 1.0
    sim_identical = mh1.jaccard_similarity(mh2)
    assert sim_identical == 1.0

    # Disjoint texts -> estimated similarity near 0.0
    sim_disjoint = mh1.jaccard_similarity(mh3)
    assert sim_disjoint < 0.1


def test_lsh_candidate_retrieval_and_determinism():
    """Verify LSH candidate retrieval and ensure deterministic hashing across index instances."""
    doc_base = "paged attention memory management for large language model serving"
    doc_near = "paged attention memory management for large language model serving with vllm"
    doc_diff = "quantum computing topological qubits condensed matter physics"

    def make_mh(text: str) -> MinHash:
        mh = MinHash(num_hashes=128, seed=123)
        mh.update(MinHash.shingle_text(text, n_gram=2))
        return mh

    mh_base = make_mh(doc_base)
    mh_near = make_mh(doc_near)
    mh_diff = make_mh(doc_diff)

    lsh1 = LSHIndex(bands=16, rows_per_band=8)
    lsh2 = LSHIndex(bands=16, rows_per_band=8)

    lsh1.insert("doc_base", mh_base)
    lsh1.insert("doc_diff", mh_diff)

    lsh2.insert("doc_base", mh_base)
    lsh2.insert("doc_diff", mh_diff)

    # Determinism: Both indices must have identical bucket keys
    assert set(lsh1.buckets.keys()) == set(lsh2.buckets.keys())

    # Query with near duplicate
    candidates1 = lsh1.query_candidates(mh_near)
    assert "doc_base" in candidates1
    assert "doc_diff" not in candidates1

    # Query similar with threshold
    results = lsh1.query_similar(mh_near, threshold=0.5)
    doc_ids = [doc_id for doc_id, _ in results]
    assert "doc_base" in doc_ids


def test_lsh_index_reindexing_and_removal():
    """Verify that updating a document's MinHash cleans up old buckets and does not match old query signatures."""
    lsh = LSHIndex(bands=16, rows_per_band=8)

    text_v1 = "distributed transactional database with multi version concurrency control"
    text_v2 = "baking sourdough bread with organic flour water salt and yeast"

    def make_sig(text: str) -> MinHash:
        mh = MinHash(num_hashes=128, seed=42)
        mh.update(MinHash.shingle_text(text, n_gram=2))
        return mh

    sig_v1 = make_sig(text_v1)
    sig_v2 = make_sig(text_v2)

    # 1. Insert doc_1 with v1 signature
    lsh.insert("doc_1", sig_v1)
    candidates_v1 = lsh.query_candidates(sig_v1)
    assert "doc_1" in candidates_v1

    # 2. Re-index doc_1 with completely different v2 signature
    lsh.insert("doc_1", sig_v2)

    # 3. Old query signature MUST NOT match doc_1 anymore! Old buckets must be cleaned up!
    candidates_after_reindex = lsh.query_candidates(sig_v1)
    assert "doc_1" not in candidates_after_reindex

    # 4. New query signature MUST match doc_1
    candidates_v2 = lsh.query_candidates(sig_v2)
    assert "doc_1" in candidates_v2

    # 5. Remove doc_1 explicitly
    removed = lsh.remove("doc_1")
    assert removed is True
    assert "doc_1" not in lsh.query_candidates(sig_v2)
    assert lsh.remove("doc_1") is False  # Already removed


def test_parameter_validations():
    with pytest.raises(ValueError):
        BloomFilter(size_m=0, hash_count_k=5)
    with pytest.raises(ValueError):
        BloomFilter(size_m=100, hash_count_k=0)
    with pytest.raises(ValueError):
        CountingBloomFilter(size_m=-1, hash_count_k=2)
    with pytest.raises(ValueError):
        MinHash(num_hashes=0)
    with pytest.raises(ValueError):
        LSHIndex(bands=0, rows_per_band=5)
