"""
Problem 16: Minimum Window Substring (Hard - Sliding Window)
Given two strings `s` and `t` of lengths $m$ and $n$ respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return empty string `""`.
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

def min_window(s: str, t: str) -> str:
    """Finds minimum window substring of s containing all characters of t.
    
    Time: O(M + N), Space: O(M + N)
    """
    raise NotImplementedError

