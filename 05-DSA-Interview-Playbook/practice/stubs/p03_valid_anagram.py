"""
Problem 3: Valid Anagram (Easy - Arrays & Hashing)
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.
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

def is_anagram(s: str, t: str) -> bool:
    """Checks if t is an anagram of s.
    
    Time: O(N), Space: O(1) assuming fixed 26-char alphabet.
    """
    raise NotImplementedError

