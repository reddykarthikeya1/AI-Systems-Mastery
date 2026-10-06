"""
Problem 2: Contains Duplicate (Easy - Arrays & Hashing)
Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.
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

def contains_duplicate(nums: list[int]) -> bool:
    """Checks if any element appears at least twice.
    
    Time: O(N), Space: O(N)
    """
    raise NotImplementedError

