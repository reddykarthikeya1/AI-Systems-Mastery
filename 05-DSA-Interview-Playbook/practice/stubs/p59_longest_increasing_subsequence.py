"""
Problem 59: Longest Increasing Subsequence (Medium - Dynamic Programming)
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.
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

def length_of_lis(nums: list[int]) -> int:
    """Finds length of longest increasing subsequence in O(N log N) time."""
    raise NotImplementedError

