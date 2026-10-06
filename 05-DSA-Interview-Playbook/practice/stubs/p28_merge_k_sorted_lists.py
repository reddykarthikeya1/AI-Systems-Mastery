"""
Problem 28: Merge K Sorted Lists (Hard - Linked List)
You are given an array of $k$ linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.
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

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """Merges k sorted linked lists using a min-heap in O(N log k) time."""
    raise NotImplementedError

