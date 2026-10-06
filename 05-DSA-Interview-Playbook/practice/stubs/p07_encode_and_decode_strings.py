"""
Problem 7: Encode and Decode Strings (Medium - Arrays & Hashing)
Design an algorithm to encode a list of strings to a single string, and decode that string back to the original list of strings. The strings can contain any possible characters, including delimiters like '#' and commas.
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

class Codec:
    def encode(self, strs: list[str]) -> str:
        raise NotImplementedError
    def decode(self, s: str) -> list[str]:
        raise NotImplementedError

