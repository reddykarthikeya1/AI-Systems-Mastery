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
def test_avl_empty_and_single_element_edge_cases():
    tree = AVLTreeEngine[int]()
    assert len(tree) == 0
    assert not tree.contains(10)
    assert tree.in_order() == []
    assert tree.validate_invariants()
    
    tree.insert(50)
    assert len(tree) == 1
    assert tree.contains(50)
    assert not tree.contains(25)
    assert tree.in_order() == [50]
    assert tree.validate_invariants()


def test_avl_all_rotations_edge_cases():
    # Left-Left rotation
    tree_ll = AVLTreeEngine[int]()
    for x in [30, 20, 10]:
        tree_ll.insert(x)
    assert tree_ll.in_order() == [10, 20, 30]
    assert tree_ll.validate_invariants()
    
    # Right-Right rotation
    tree_rr = AVLTreeEngine[int]()
    for x in [10, 20, 30]:
        tree_rr.insert(x)
    assert tree_rr.in_order() == [10, 20, 30]
    assert tree_rr.validate_invariants()
    
    # Left-Right rotation
    tree_lr = AVLTreeEngine[int]()
    for x in [30, 10, 20]:
        tree_lr.insert(x)
    assert tree_lr.in_order() == [10, 20, 30]
    assert tree_lr.validate_invariants()
    
    # Right-Left rotation
    tree_rl = AVLTreeEngine[int]()
    for x in [10, 30, 20]:
        tree_rl.insert(x)
    assert tree_rl.in_order() == [10, 20, 30]
    assert tree_rl.validate_invariants()
