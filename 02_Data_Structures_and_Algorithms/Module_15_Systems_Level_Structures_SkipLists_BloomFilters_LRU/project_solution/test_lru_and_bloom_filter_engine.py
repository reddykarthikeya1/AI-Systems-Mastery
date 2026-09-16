"""Unit tests for LRUAndBloomFilterEngine."""
import pytest
from lru_and_bloom_filter_engine import BloomFilter, LRUCache


def test_lru_eviction_order():
    cache = LRUCache[str, int](capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1  # Accesses 'a', making 'b' least recently used

    cache.put("c", 3)  # Evicts 'b'
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    with pytest.raises(KeyError):
        cache.get("b")

def test_lru_update_value():
    cache = LRUCache[str, int](capacity=2)
    cache.put("k1", 10)
    cache.put("k1", 20)
    assert cache.get("k1") == 20
    assert len(cache) == 1

def test_bloom_filter_no_false_negatives():
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
    inserted = [f"item_{i}" for i in range(100)]
    for item in inserted:
        bf.add(item)

    # Invariant: 0 false negatives
    for item in inserted:
        assert bf.contains(item)

    # Test absent elements
    absent = [f"missing_{i}" for i in range(100)]
    false_positives = sum(1 for item in absent if bf.contains(item))
    # Should have <= 5% false positives under 1% theoretical rate
    assert false_positives <= 5

def test_lru_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache[str, int](0)
    with pytest.raises(ValueError):
        LRUCache[str, int](-5)

def test_bloom_filter_invalid_args():
    with pytest.raises(ValueError):
        BloomFilter(0, 0.01)
    with pytest.raises(ValueError):
        BloomFilter(100, 1.5)
