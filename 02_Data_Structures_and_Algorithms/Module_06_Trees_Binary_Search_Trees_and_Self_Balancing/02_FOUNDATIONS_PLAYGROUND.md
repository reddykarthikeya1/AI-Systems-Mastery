# 🐣 Interactive Foundations Playground: Binary Trees & BST Properties

> *"A tree is an inverted family hierarchy: one root at the top, branching out to leaves at the bottom."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from dataclasses import dataclass
from typing import Optional
```

---

## 1. Binary Tree Representation and Recursive Depth

Each tree node holds a value and left/right child pointers. Maximum depth is calculated recursively as $1 + \max(\text{depth}(L), \text{depth}(R))$.

```python
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
```

---

## 2. In-Order Traversal of a Binary Search Tree

In a BST, every node in the left subtree is smaller than root, and every node in the right subtree is greater. In-order traversal visits nodes in strictly sorted order.

```python
def inorder(node):
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

traversed = inorder(root)
assert traversed == [1, 2, 3, 4, 5, 6, 7], "Inorder of BST must be sorted"
assert traversed == sorted(traversed)
print(f"Inorder traversal yields sorted order: {traversed}")
```

---

## 3. Logarithmic Search in a BST

At each node, comparing the search target against the current value eliminates half of the remaining subtree, yielding $O(\log N)$ average search.

```python
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
```

---
