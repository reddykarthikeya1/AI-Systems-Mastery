"""
Problem 9: Valid Palindrome (Easy - Two Pointers)
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.
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

def is_palindrome(s: str) -> bool:
    """Checks if string is palindrome ignoring non-alphanumeric chars.
    
    Time: O(N), Space: O(1)
    """
    raise NotImplementedError

