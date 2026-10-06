"""
Problem 37: Construct Binary Tree from Preorder and Inorder Traversal (Medium - Trees)
Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.
"""
from typing import List, Dict, Optional, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    """Reconstructs binary tree in O(N) time using index map."""
    in_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = 0
    
    def helper(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre_idx
        if left > right:
            return None
            
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        
        mid = in_map[root_val]
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root
        
    return helper(0, len(inorder) - 1)


def run_tests():
    t = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert t.val == 3
    assert t.left.val == 9
    assert t.right.val == 20
    assert t.right.left.val == 15
    assert build_tree([-1], [-1]).val == -1
    assert build_tree([], []) is None
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p37_construct_binary_tree_from_preorder_and_inorder_traversal!")
