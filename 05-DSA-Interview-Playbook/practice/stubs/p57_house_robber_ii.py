"""
Problem 57: House Robber II (Medium - Dynamic Programming)
You are a professional robber planning to rob houses along a street, but all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Determine the maximum amount of money you can rob tonight without alerting the police.
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

def rob_circular(nums: list[int]) -> int:
    """Solves circular house robber problem in O(N) time, O(1) space."""
    raise NotImplementedError

