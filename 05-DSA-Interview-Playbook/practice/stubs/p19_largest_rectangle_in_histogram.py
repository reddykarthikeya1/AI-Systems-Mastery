"""
Problem 19: Largest Rectangle in Histogram (Hard - Stack)
Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
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

def largest_rectangle_area(heights: list[int]) -> int:
    """Computes maximum rectangle area using a monotonic increasing stack.
    
    Time: O(N), Space: O(N)
    """
    raise NotImplementedError

