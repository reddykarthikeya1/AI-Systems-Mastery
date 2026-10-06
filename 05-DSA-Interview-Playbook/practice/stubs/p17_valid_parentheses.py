"""
Problem 17: Valid Parentheses (Easy - Stack)
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.
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

def is_valid_parentheses(s: str) -> bool:
    """Checks if bracket sequence is properly nested and closed.
    
    Time: O(N), Space: O(N)
    """
    raise NotImplementedError

