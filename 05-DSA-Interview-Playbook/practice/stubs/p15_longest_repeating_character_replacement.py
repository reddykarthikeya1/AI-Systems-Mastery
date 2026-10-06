"""
Problem 15: Longest Repeating Character Replacement (Medium - Sliding Window)
You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times. Return the length of the longest substring containing the same letter you can get after performing above operations.
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

def character_replacement(s: str, k: int) -> int:
    """Finds longest repeating character substring after at most k replacements.
    
    Time: O(N), Space: O(1)
    """
    raise NotImplementedError

