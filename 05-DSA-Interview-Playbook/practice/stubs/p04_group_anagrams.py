"""
Problem 4: Group Anagrams (Medium - Arrays & Hashing)
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.
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

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Groups strings that are anagrams of each other.
    
    Time: O(N * K), Space: O(N * K)
    """
    raise NotImplementedError

