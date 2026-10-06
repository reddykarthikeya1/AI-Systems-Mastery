"""
Problem 75: Missing Number (Easy - Bit Manipulation)
Given an array `nums` containing $n$ distinct numbers in the range $[0, n]$, return the only number in the range that is missing from the array.
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

def missing_number(nums: list[int]) -> int:
    """Finds missing number in O(N) time, O(1) space using XOR."""
    raise NotImplementedError

