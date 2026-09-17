"""Unit tests for RobinHoodHashMap."""
import pytest
from robin_hood_hash_map import RobinHoodHashMap


def test_basic_crud():
    hm = RobinHoodHashMap[str, int](initial_capacity=8)
    assert len(hm) == 0
    hm.put("apple", 100)
    hm.put("banana", 200)
    assert len(hm) == 2
    assert hm.get("apple") == 100
    assert hm.get("banana") == 200
    assert "apple" in hm
    assert "cherry" not in hm

    # Update value
    hm.put("apple", 999)
    assert hm.get("apple") == 999
    assert len(hm) == 2

    # Delete
    removed = hm.remove("apple")
    assert removed == 999
    assert len(hm) == 1
    assert "apple" not in hm
    with pytest.raises(KeyError):
        hm.get("apple")

def test_rehash_and_scale():
    hm = RobinHoodHashMap[int, str](initial_capacity=4)
    for i in range(20):
        hm.put(i, f"val_{i}")
    assert len(hm) == 20
    assert hm.capacity > 4
    for i in range(20):
        assert hm.get(i) == f"val_{i}"

def test_backward_shift_integrity():
    hm = RobinHoodHashMap[int, int](initial_capacity=16)
    # Insert multiple keys
    for k in range(10):
        hm.put(k, k * 10)
    for k in [2, 5, 7]:
        hm.remove(k)
    for k in range(10):
        if k in [2, 5, 7]:
            assert k not in hm
        else:
            assert hm.get(k) == k * 10

def test_empty_map():
    hm = RobinHoodHashMap[str, int]()
    assert len(hm) == 0
    with pytest.raises(KeyError):
        hm.get("nonexistent")

def test_duplicate_key_updates():
    hm = RobinHoodHashMap[str, int]()
    hm.put("x", 1)
    hm.put("x", 2)
    hm.put("x", 3)
    assert len(hm) == 1
    assert hm.get("x") == 3

def test_delete_nonexistent_key():
    hm = RobinHoodHashMap[str, int]()
    with pytest.raises(KeyError):
        hm.remove("ghost")
def test_robin_hood_edge_cases():
    hm = RobinHoodHashMap[str, int](initial_capacity=4)
    # Nonexistent key raises KeyError
    with pytest.raises(KeyError):
        hm.get("missing")
    with pytest.raises(KeyError):
        hm.remove("missing")
    
    # Duplicate key updates value without altering count
    hm.put("key1", 100)
    assert len(hm) == 1
    assert hm.get("key1") == 100
    hm.put("key1", 200)
    assert len(hm) == 1
    assert hm.get("key1") == 200
    
    # Delete and re-insert
    val = hm.remove("key1")
    assert val == 200
    assert len(hm) == 0
    with pytest.raises(KeyError):
        hm.get("key1")
    hm.put("key1", 300)
    assert len(hm) == 1
    assert hm.get("key1") == 300


def test_robin_hood_collision_cascade_and_growth():
    hm = RobinHoodHashMap[int, str](initial_capacity=4)
    # Insert keys that force Robin Hood swaps
    for i in range(20):
        hm.put(i, f"val_{i}")
        assert hm.get(i) == f"val_{i}"
    assert len(hm) == 20
    for i in range(20):
        assert hm.get(i) == f"val_{i}"
        assert hm.remove(i) == f"val_{i}"
    assert len(hm) == 0

