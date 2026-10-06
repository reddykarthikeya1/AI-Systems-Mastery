"""
Problem 1: Two Sum (Easy - Arrays & Hashing)
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you may not use the same element twice.
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

def two_sum(nums: list[int], target: int) -> list[int]:
    """Finds indices of two numbers that add up to target.
    
    Time: O(N), Space: O(N)
    """
    raise NotImplementedError

