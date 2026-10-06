"""
Problem 25: Reorder List (Medium - Linked List)
You are given the head of a singly linked-list: $L_0 \to L_1 \to \dots \to L_{n - 1} \to L_n$. Reorder the list to: $L_0 \to L_n \to L_1 \to L_{n - 1} \to L_2 \to L_{n - 2} \dots$ in-place without modifying node values.
"""
from typing import List, Dict, Optional, Tuple, Set

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def reorder_list(head: Optional[ListNode]) -> None:
    """Reorders list in-place to L0 -> Ln -> L1 -> Ln-1 ..."""
    raise NotImplementedError

