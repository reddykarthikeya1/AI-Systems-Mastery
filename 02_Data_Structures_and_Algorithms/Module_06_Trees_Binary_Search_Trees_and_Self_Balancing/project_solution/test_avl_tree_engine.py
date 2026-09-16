"""Unit tests for AVLTreeEngine."""
from avl_tree_engine import AVLTreeEngine


def test_avl_rotations_and_balancing():
    tree = AVLTreeEngine[int]()
    # Insert in strictly ascending order (would produce linked-list degenerate tree in naive BST)
    for x in [10, 20, 30, 40, 50, 25]:
        tree.insert(x)

    assert len(tree) == 6
    assert tree.validate_invariants()
    # In-order traversal must be strictly sorted
    assert tree.in_order() == [10, 20, 25, 30, 40, 50]

def test_avl_contains():
    tree = AVLTreeEngine[str]()
    for s in ["zebra", "apple", "mango", "banana", "peach"]:
        tree.insert(s)
    assert tree.contains("apple")
    assert tree.contains("peach")
    assert not tree.contains("grape")
    assert tree.validate_invariants()

def test_empty_tree():
    tree = AVLTreeEngine[int]()
    assert len(tree) == 0
    assert tree.in_order() == []
    assert not tree.contains(10)
    assert tree.validate_invariants()

def test_descending_insertion_rotations():
    tree = AVLTreeEngine[int]()
    for x in [50, 40, 30, 20, 10]:
        tree.insert(x)
    assert len(tree) == 5
    assert tree.validate_invariants()
    assert tree.in_order() == [10, 20, 30, 40, 50]

def test_duplicate_insertions():
    tree = AVLTreeEngine[int]()
    tree.insert(5)
    tree.insert(5)
    assert len(tree) == 2
    assert tree.validate_invariants()
