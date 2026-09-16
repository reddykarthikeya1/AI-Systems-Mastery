"""Module 06: Interactive Trees CLI Sandbox."""
from __future__ import annotations


class TreeNode:
    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None):
        self.val = val
        self.left = left
        self.right = right


def inorder(root: TreeNode | None) -> list[int]:
    return [*inorder(root.left), root.val, *inorder(root.right)] if root else []


def demo():
    print("\n=== DEMO: BST Inorder Traversal Gives Sorted Array! ===")
    root = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6)), TreeNode(10, None, TreeNode(14)))
    print("BST Inorder Traversal:", inorder(root))


if __name__ == "__main__":
    demo()
