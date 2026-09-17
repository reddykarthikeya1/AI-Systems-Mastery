"""Unit tests for MonotonicQueueEngine."""
import pytest
from monotonic_queue_engine import MinMaxStack, MonotonicQueue


def test_min_max_stack():
    s = MinMaxStack[int]()
    s.push(5)
    assert s.get_min() == 5
    assert s.get_max() == 5

    s.push(2)
    s.push(10)
    assert s.get_min() == 2
    assert s.get_max() == 10
    assert s.top() == 10

    assert s.pop() == 10
    assert s.get_max() == 5
    assert s.get_min() == 2

    assert s.pop() == 2
    assert s.get_min() == 5
    assert s.get_max() == 5

    assert s.pop() == 5
    with pytest.raises(IndexError):
        s.pop()

def test_monotonic_queue_sliding_window():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    mq = MonotonicQueue()
    result: list[int] = []

    for i in range(len(nums)):
        mq.push(nums[i])
        if i >= k - 1:
            result.append(mq.max())
            mq.pop(nums[i - k + 1])

    assert result == [3, 3, 5, 5, 6, 7]

def test_min_max_stack_empty_errors():
    s = MinMaxStack[int]()
    with pytest.raises(IndexError):
        s.top()
    with pytest.raises(IndexError):
        s.get_min()
    with pytest.raises(IndexError):
        s.get_max()

def test_monotonic_queue_empty_error():
    mq = MonotonicQueue()
    with pytest.raises(IndexError):
        mq.max()

def test_monotonic_queue_strictly_decreasing():
    mq = MonotonicQueue()
    for x in [5, 4, 3, 2, 1]:
        mq.push(x)
    assert mq.max() == 5
    assert len(mq) == 5

def test_monotonic_queue_strictly_increasing():
    mq = MonotonicQueue()
    for x in [1, 2, 3, 4, 5]:
        mq.push(x)
    assert mq.max() == 5
    assert len(mq) == 1
def test_min_max_stack_edge_cases():
    st = MinMaxStack[int]()
    with pytest.raises(IndexError):
        st.pop()
    with pytest.raises(IndexError):
        st.top()
    with pytest.raises(IndexError):
        st.get_min()
    with pytest.raises(IndexError):
        st.get_max()
    
    # All identical elements
    for _ in range(4):
        st.push(7)
    assert st.get_min() == 7
    assert st.get_max() == 7
    for _ in range(4):
        assert st.pop() == 7


def test_monotonic_queue_edge_cases():
    mq = MonotonicQueue()
    # pop on empty is safe no-op
    mq.pop(0)
    with pytest.raises(IndexError):
        mq.max()

    
    # Monotonically strictly decreasing stream
    for x in [10, 8, 6, 4, 2]:
        mq.push(x)
    assert mq.max() == 10
    
    # Push larger element to evict everything
    mq.push(100)
    assert mq.max() == 100
    
    # Pop non-max values doesn't drop max
    mq.pop(100)
    assert len(mq) == 0
    with pytest.raises(IndexError):
        mq.max()

