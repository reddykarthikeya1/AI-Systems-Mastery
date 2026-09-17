"""Beginner playground for Module 06 - Binary Trees & BST Properties.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# -------------------------------------------- 1. Binary Tree Representation and Recursive Depth
@dataclass
class TreeNode:
    val: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None

root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5), TreeNode(7)))

def max_depth(node):
    if not node:
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))

assert max_depth(root) == 3
assert max_depth(None) == 0
print(f"Calculated maximum depth of balanced tree: {max_depth(root)}")

# -------------------------------------------- 2. In-Order Traversal of a Binary Search Tree
def inorder(node):
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

traversed = inorder(root)
assert traversed == [1, 2, 3, 4, 5, 6, 7], "Inorder of BST must be sorted"
assert traversed == sorted(traversed)
print(f"Inorder traversal yields sorted order: {traversed}")

# -------------------------------------------- 3. Logarithmic Search in a BST
def bst_search(node, target):
    if not node or node.val == target:
        return node is not None
    if target < node.val:
        return bst_search(node.left, target)
    return bst_search(node.right, target)

assert bst_search(root, 5) is True
assert bst_search(root, 99) is False
assert bst_search(root, 1) is True
print("BST search verified: 5 found, 99 not found, 1 found.")

print()
print("All checks passed.")
