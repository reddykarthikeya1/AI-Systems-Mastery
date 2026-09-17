"""Unit tests for DoublyLinkedListEngine."""
import pytest
from doubly_linked_list_engine import DoublyLinkedListEngine


def test_initialization():
    dll = DoublyLinkedListEngine[int]()
    assert len(dll) == 0
    assert dll.to_list() == []
    assert not dll.has_cycle()

def test_push_and_pop_front():
    dll = DoublyLinkedListEngine[int]()
    dll.push_front(10)
    dll.push_front(20)
    assert len(dll) == 2
    assert dll.to_list() == [20, 10]
    assert dll.pop_front() == 20
    assert dll.pop_front() == 10
    assert len(dll) == 0
    with pytest.raises(IndexError):
        dll.pop_front()

def test_push_and_pop_back():
    dll = DoublyLinkedListEngine[str]()
    dll.push_back("a")
    dll.push_back("b")
    dll.push_back("c")
    assert len(dll) == 3
    assert dll.to_list() == ["a", "b", "c"]
    assert dll.pop_back() == "c"
    assert dll.to_list() == ["a", "b"]

def test_reverse():
    dll = DoublyLinkedListEngine[int]()
    for x in [1, 2, 3, 4, 5]:
        dll.push_back(x)
    dll.reverse()
    assert dll.to_list() == [5, 4, 3, 2, 1]
    assert dll.pop_front() == 5
    assert dll.pop_back() == 1
    assert dll.to_list() == [4, 3, 2]

def test_cycle_detection():
    dll = DoublyLinkedListEngine[int]()
    for x in range(5):
        dll.push_back(x)
    assert not dll.has_cycle()

def test_empty_pop_back():
    dll = DoublyLinkedListEngine[int]()
    with pytest.raises(IndexError):
        dll.pop_back()

def test_single_element_reverse():
    dll = DoublyLinkedListEngine[int]()
    dll.push_back(99)
    dll.reverse()
    assert dll.to_list() == [99]

def test_iteration_protocol():
    dll = DoublyLinkedListEngine[int]()
    for x in [10, 20, 30]:
        dll.push_back(x)
    assert list(dll) == [10, 20, 30]
def test_cycle_detection_with_actual_cycle():
    dll = DoublyLinkedListEngine[int]()
    for x in [1, 2, 3, 4]:
        dll.push_back(x)
    assert not dll.has_cycle()
    
    # Inject cycle among real data nodes
    last_real = dll._tail.prev
    first_real = dll._head.next
    last_real.next = first_real
    assert dll.has_cycle()
    
    # Restore pointer to sentinel tail
    last_real.next = dll._tail
    assert not dll.has_cycle()



def test_single_element_and_empty_edge_cases():
    dll = DoublyLinkedListEngine[int]()
    assert dll.to_list() == []
    dll.reverse()
    assert dll.to_list() == []
    
    # Push front, pop back
    dll.push_front(99)
    assert len(dll) == 1
    assert dll.pop_back() == 99
    assert len(dll) == 0
    
    # Push back, pop front
    dll.push_back(77)
    assert len(dll) == 1
    assert dll.pop_front() == 77
    assert len(dll) == 0
