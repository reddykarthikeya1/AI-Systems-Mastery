"""
Problem 42: Kth Largest Element in an Array (Medium - Heap / Priority Queue)
Given an integer array `nums` and an integer `k`, return the $k^{\text{th}}$ largest element in the array. Note that it is the $k^{\text{th}}$ largest element in sorted order, not the $k^{\text{th}}$ distinct element.
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

def find_kth_largest(nums: list[int], k: int) -> int:
    """Finds kth largest element using min-heap in O(N log k) time."""
    raise NotImplementedError

