"""
Problem 14: Longest Substring Without Repeating Characters (Medium - Sliding Window)
Given a string `s`, find the length of the longest substring without duplicate characters.
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

def length_of_longest_substring(s: str) -> int:
    """Finds length of longest substring without duplicate characters.
    
    Time: O(N), Space: O(min(N, M))
    """
    raise NotImplementedError

