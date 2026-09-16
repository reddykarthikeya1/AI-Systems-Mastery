"""Problem-bank suite for Module_06_Trees_Binary_Search_Trees_and_Self_Balancing.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_inorder_traversal import inorder_traversal
from p02_level_order import level_order
from p03_max_depth import max_depth
from p04_is_valid_bst import is_valid_bst
from p05_lca_bst import lca_bst
from p06_kth_smallest_bst import kth_smallest_bst
from p07_is_balanced import is_balanced
from p08_tree_diameter import tree_diameter
from tree_common import TreeNode, find_node, from_level_order


def test_p01_inorder_traversal():
    """Iterative Inorder Traversal — Explicit stack traversal (Medium)."""
    assert inorder_traversal(from_level_order([1, None, 2, 3])) == [1, 3, 2]
    assert inorder_traversal(None) == []
    assert inorder_traversal(from_level_order([1])) == [1]
    assert inorder_traversal(from_level_order([2, 1, 3])) == [1, 2, 3]
    # A BST's inorder traversal is sorted - that is the defining property.
    bst = from_level_order([8, 4, 12, 2, 6, 10, 14])
    assert inorder_traversal(bst) == sorted(inorder_traversal(bst))
    # Degenerate left chain, deep enough to break a recursive solution, # if it were written recursively.
    left_chain = TreeNode(0)
    node = left_chain
    for i in range(1, 5000):
        node.left = TreeNode(i)
        node = node.left
    assert inorder_traversal(left_chain) == list(range(4999, -1, -1))

def test_p02_level_order():
    """Level Order Traversal — BFS (Medium)."""
    assert level_order(from_level_order([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert level_order(None) == []
    assert level_order(from_level_order([1])) == [[1]]
    # A pure left chain gives one node per level.
    assert level_order(from_level_order([1, 2, None, 3])) == [[1], [2], [3]]
    # A complete tree.
    assert level_order(from_level_order([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]
    # Level widths must match the tree's actual shape.
    got = level_order(from_level_order([1, 2, 3, 4, None, None, 7]))
    assert [len(lv) for lv in got] == [1, 2, 2]

def test_p03_max_depth():
    """Maximum Depth — Tree recursion (Easy)."""
    assert max_depth(from_level_order([3, 9, 20, None, None, 15, 7])) == 3
    assert max_depth(None) == 0
    assert max_depth(from_level_order([1])) == 1
    assert max_depth(from_level_order([1, 2])) == 2
    assert max_depth(from_level_order([1, None, 2])) == 2
    # Depth counts NODES, not edges - a 3-node chain has depth 3.
    assert max_depth(from_level_order([1, 2, None, 3])) == 3
    # A complete tree of 7 nodes has depth 3.
    assert max_depth(from_level_order([1, 2, 3, 4, 5, 6, 7])) == 3

def test_p04_is_valid_bst():
    """Validate A Binary Search Tree — Range invariant propagation (Medium)."""
    assert is_valid_bst(from_level_order([2, 1, 3])) is True
    # The case a local parent/child check wrongly accepts.
    assert is_valid_bst(from_level_order([5, 1, 4, None, None, 3, 6])) is False
    assert is_valid_bst(None) is True
    assert is_valid_bst(from_level_order([1])) is True
    # A violation buried deep on the left.
    assert is_valid_bst(from_level_order([10, 5, 15, 2, 20])) is False
    # Valid, with a deep right spine.
    assert is_valid_bst(from_level_order([1, None, 2, None, 3])) is True
    # Equal values are not allowed by a strict BST.
    root = TreeNode(2, TreeNode(2), TreeNode(3))
    assert is_valid_bst(root) is False
    # Cross-check: a tree is a BST exactly when its inorder walk is, # strictly increasing.
    def _inorder(n):
        return [*_inorder(n.left), n.val, *_inorder(n.right)] if n else []
    for spec in (
        [8, 4, 12, 2, 6, 10, 14],
        [5, 1, 4, None, None, 3, 6],
        [10, 5, 15, None, None, 6, 20],
        [3, 1, 5, 0, 2, 4, 6],
    ):
        t = from_level_order(spec)
        vals = _inorder(t)
        expected = all(a < b for a, b in zip(vals, vals[1:]))
        assert is_valid_bst(t) is expected, spec

def test_p05_lca_bst():
    """Lowest Common Ancestor In A BST — BST invariant walk (Medium)."""
    tree = from_level_order([6, 2, 8, 0, 4, 7, 9])
    assert lca_bst(tree, 2, 8).val == 6
    assert lca_bst(tree, 2, 4).val == 2
    assert lca_bst(tree, 0, 4).val == 2
    assert lca_bst(tree, 7, 9).val == 8
    assert lca_bst(tree, 0, 9).val == 6
    # A node is a descendant of itself.
    assert lca_bst(tree, 6, 2).val == 6
    # Argument order must not matter.
    assert lca_bst(tree, 8, 2).val == 6
    assert lca_bst(tree, 4, 0).val == 2
    assert lca_bst(None, 1, 2) is None
    # The returned node must be the real node in the tree.
    assert lca_bst(tree, 2, 4) is find_node(tree, 2)
    # O(height): a right spine of 10**4 nodes must still be fast.
    spine = TreeNode(0)
    node = spine
    for i in range(1, 10_000):
        node.right = TreeNode(i)
        node = node.right
    assert lca_bst(spine, 9998, 9999).val == 9998

def test_p06_kth_smallest_bst():
    """K-th Smallest Element In A BST — Inorder with early exit (Medium)."""
    assert kth_smallest_bst(from_level_order([3, 1, 4, None, 2]), 1) == 1
    assert kth_smallest_bst(from_level_order([3, 1, 4, None, 2]), 2) == 2
    assert kth_smallest_bst(from_level_order([3, 1, 4, None, 2]), 4) == 4
    tree = from_level_order([5, 3, 6, 2, 4, None, None, 1])
    assert kth_smallest_bst(tree, 3) == 3
    assert kth_smallest_bst(tree, 1) == 1
    assert kth_smallest_bst(tree, 6) == 6
    # Single node.
    assert kth_smallest_bst(from_level_order([42]), 1) == 42
    # Out of range must raise, not return None.
    with pytest.raises(ValueError):
        kth_smallest_bst(from_level_order([1, None, 2]), 3)
    with pytest.raises(ValueError):
        kth_smallest_bst(from_level_order([1]), 0)
    with pytest.raises(ValueError):
        kth_smallest_bst(None, 1)
    # Every k must agree with the sorted inorder list.
    bst = from_level_order([8, 4, 12, 2, 6, 10, 14])
    for i, expected in enumerate([2, 4, 6, 8, 10, 12, 14], start=1):
        assert kth_smallest_bst(bst, i) == expected
    # Early exit: a 10**4-node left spine with k=1 must be fast, which, # it is only if the traversal stops immediately.
    spine = TreeNode(10_000)
    node = spine
    for i in range(9_999, 0, -1):
        node.left = TreeNode(i)
        node = node.left
    assert kth_smallest_bst(spine, 1) == 1

def test_p07_is_balanced():
    """Height-Balanced Binary Tree — Bottom-up recursion (Medium)."""
    assert is_balanced(from_level_order([3, 9, 20, None, None, 15, 7])) is True
    assert is_balanced(from_level_order([1, 2, 2, 3, 3, None, None, 4, 4])) is False
    assert is_balanced(None) is True
    assert is_balanced(from_level_order([1])) is True
    assert is_balanced(from_level_order([1, 2])) is True
    # A 3-node chain differs by 2 at the root.
    assert is_balanced(from_level_order([1, 2, None, 3])) is False
    # Imbalance deep in the tree, with a balanced root.
    deep = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))), TreeNode(5))
    assert is_balanced(deep) is False
    # Complete trees are always balanced.
    assert is_balanced(from_level_order([1, 2, 3, 4, 5, 6, 7])) is True
    # O(n): the naive recompute-height-at-every-node approach is
    # O(n^2) on a spine and would be far slower than this.
    # Depth 900 stays inside Python's 1000-frame recursion limit -
    spine = TreeNode(0)
    node = spine
    for i in range(1, 900):
        node.left = TreeNode(i)
        node = node.left
    assert is_balanced(spine) is False

def test_p08_tree_diameter():
    """Diameter Of A Binary Tree — Bottom-up recursion with a running best (Hard)."""
    assert tree_diameter(from_level_order([1, 2, 3, 4, 5])) == 3
    assert tree_diameter(from_level_order([1, 2])) == 1
    assert tree_diameter(from_level_order([1])) == 0
    assert tree_diameter(None) == 0
    # The diameter need not pass through the root.
    skewed = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4)), TreeNode(5)))
    assert tree_diameter(skewed) == 3
    # A pure chain of n nodes has diameter n-1 edges.
    chain = TreeNode(0)
    node = chain
    for i in range(1, 100):
        node.right = TreeNode(i)
        node = node.right
    assert tree_diameter(chain) == 99
    # A complete tree of depth 3: leaf up to root and down again.
    assert tree_diameter(from_level_order([1, 2, 3, 4, 5, 6, 7])) == 4
