"""
Problem 56: House Robber (Medium - Dynamic Programming)
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent houses were broken into on the same night. Determine the maximum amount of money you can rob tonight without alerting the police.
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

def rob(nums: list[int]) -> int:
    """Finds max non-adjacent house loot in O(N) time, O(1) space."""
    raise NotImplementedError

