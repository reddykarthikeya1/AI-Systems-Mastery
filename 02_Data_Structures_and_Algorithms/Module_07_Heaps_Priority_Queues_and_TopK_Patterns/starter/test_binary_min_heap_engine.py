"""Unit tests for BinaryMinHeapEngine."""
import pytest
from binary_min_heap_engine import BinaryMinHeap, TopKTracker


def test_heap_push_pop():
    h = BinaryMinHeap[int]()
    for x in [30, 10, 50, 20, 5]:
        h.push(x)

    assert len(h) == 5
    assert h.peek() == 5
    extracted = [h.pop() for _ in range(5)]
    assert extracted == [5, 10, 20, 30, 50]
    with pytest.raises(IndexError):
        h.pop()

def test_heapify_linear_time():
    data = [42, 12, 88, 1, 9, 33, 100, 7]
    h = BinaryMinHeap.heapify(data)
    assert len(h) == len(data)
    extracted = [h.pop() for _ in range(len(data))]
    assert extracted == sorted(data)

def test_top_k_streaming():
    tracker = TopKTracker(k=3)
    stream = [10, 5, 20, 3, 100, 50, 2, 70]
    for val in stream:
        tracker.add(val)
    # Top 3 largest elements: 100, 70, 50
    assert tracker.get_top_k() == [100, 70, 50]

def test_empty_heap_peek():
    h = BinaryMinHeap[int]()
    with pytest.raises(IndexError):
        h.peek()

def test_top_k_invalid_k():
    with pytest.raises(ValueError):
        TopKTracker(k=0)
    with pytest.raises(ValueError):
        TopKTracker(k=-1)

def test_top_k_with_fewer_elements_than_k():
    tracker = TopKTracker(k=5)
    tracker.add(10)
    tracker.add(20)
    assert tracker.get_top_k() == [20, 10]
def test_heap_empty_and_single_element_edge_cases():
    heap = BinaryMinHeap[int]()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.pop()
    with pytest.raises(IndexError):
        heap.peek()
    
    heap.push(42)
    assert len(heap) == 1
    assert heap.peek() == 42
    assert heap.pop() == 42
    assert len(heap) == 0


def test_heap_all_duplicates_and_reverse_order():
    heap = BinaryMinHeap[int]()
    # Duplicates
    for _ in range(5):
        heap.push(10)
    for _ in range(5):
        assert heap.pop() == 10
    
    # Reverse sorted input
    for x in [50, 40, 30, 20, 10]:
        heap.push(x)
    res = [heap.pop() for _ in range(5)]
    assert res == [10, 20, 30, 40, 50]


def test_top_k_tracker_edge_cases():
    tracker = TopKTracker(k=3)
    # Fewer than k items

    tracker.add(10)
    assert tracker.get_top_k() == [10]
    tracker.add(20)
    assert sorted(tracker.get_top_k(), reverse=True) == [20, 10]
    # Exactly k
    tracker.add(30)
    assert sorted(tracker.get_top_k(), reverse=True) == [30, 20, 10]
    # More than k
    tracker.add(5)
    assert sorted(tracker.get_top_k(), reverse=True) == [30, 20, 10]
    tracker.add(40)
    assert sorted(tracker.get_top_k(), reverse=True) == [40, 30, 20]
