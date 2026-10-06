"""
Problem 12: Trapping Rain Water (Hard - Two Pointers)
Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
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

def trap_rain_water(height: list[int]) -> int:
    """Computes trapped rain water in O(N) time and O(1) space.
    
    Time: O(N), Space: O(1)
    """
    raise NotImplementedError

