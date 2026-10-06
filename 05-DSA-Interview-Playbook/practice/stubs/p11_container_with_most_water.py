"""
Problem 11: Container With Most Water (Medium - Two Pointers)
You are given an integer array `height` of length $n$. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.
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

def max_area(height: list[int]) -> int:
    """Finds maximum water container capacity using two pointers.
    
    Time: O(N), Space: O(1)
    """
    raise NotImplementedError

