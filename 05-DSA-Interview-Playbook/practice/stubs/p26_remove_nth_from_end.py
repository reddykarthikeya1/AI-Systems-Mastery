"""
Problem 26: Remove Nth Node From End of List (Medium - Linked List)
Given the `head` of a linked list, remove the $n^{\text{th}}$ node from the end of the list and return its head in one single pass.
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

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Removes nth node from end of list in a single pass."""
    raise NotImplementedError

