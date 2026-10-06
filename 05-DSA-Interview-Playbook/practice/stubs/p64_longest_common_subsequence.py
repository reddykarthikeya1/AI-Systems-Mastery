"""
Problem 64: Longest Common Subsequence (Medium - Dynamic Programming)
Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.
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

def longest_common_subsequence(text1: str, text2: str) -> int:
    """Computes LCS length in O(M * N) time using 2D DP."""
    raise NotImplementedError

