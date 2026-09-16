#!/usr/bin/env python3
"""Tree validation. Exits 0, and approves trees that are not BSTs.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

from collections import deque

RULE = "=" * 68


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val=0, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


def from_level_order(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            v = values[i]; i += 1
            if v is not None:
                node.left = TreeNode(v); queue.append(node.left)
        if i < len(values):
            v = values[i]; i += 1
            if v is not None:
                node.right = TreeNode(v); queue.append(node.right)
    return root


def inorder(node):
    return inorder(node.left) + [node.val] + inorder(node.right) if node else []


def is_valid_bst(root) -> bool:
    if root is None:
        return True
    if root.left is not None and root.left.val >= root.val:
        return False
    if root.right is not None and root.right.val <= root.val:
        return False
    return is_valid_bst(root.left) and is_valid_bst(root.right)


def max_depth(root) -> int:
    if root is None:
        return 1
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_balanced(root) -> bool:
    def height(node):
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if root is None:
        return True
    return abs(height(root.left) - height(root.right)) <= 1


def level_order(root):
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        out.append([node.val])
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return out


def main() -> None:
    print(RULE)
    print("TREE VALIDATION SERVICE")
    print(RULE)

    print()
    print("[1] BST validation")
    specs = [
        ([2, 1, 3], True),
        ([5, 1, 4, None, None, 3, 6], False),
        ([10, 5, 15, None, None, 6, 20], False),
        ([3, 1, 5, 0, 2, 4, 6], True),
    ]
    for spec, expected in specs:
        tree = from_level_order(spec)
        vals = inorder(tree)
        truth = all(a < b for a, b in zip(vals, vals[1:]))
        print(f"      {spec}")
        print(f"          reported {is_valid_bst(tree)!s:<6} inorder {vals} "
              f"strictly increasing = {truth}")

    print()
    print("[2] Maximum depth")
    for spec, expected in (([3, 9, 20, None, None, 15, 7], 3), ([1], 1), ([], 0),
                           ([1, 2], 2)):
        print(f"      {spec} -> {max_depth(from_level_order(spec))} (expected {expected})")

    print()
    print("[3] Height balance")
    specs = [
        ([3, 9, 20, None, None, 15, 7], True),
        ([1, 2, 2, 3, 3, None, None, 4, 4], False),
        ([1, 2, None, 3], False),
    ]
    for spec, expected in specs:
        print(f"      {spec} -> {is_balanced(from_level_order(spec))} (expected {expected})")
    deep = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))), TreeNode(5))
    print(f"      root balanced but left subtree deep -> {is_balanced(deep)} (expected False)")

    print()
    print("[4] Level order grouping")
    for spec, expected in (([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
                           ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]])):
        print(f"      {spec}")
        print(f"          reported {level_order(from_level_order(spec))}")
        print(f"          expected {expected}")

    print()
    print(RULE)
    print("Validation complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
