"""
Problem 73: Number of 1 Bits (Easy - Bit Manipulation)
Given a positive integer `n`, write a function that returns the number of set bits (1s) it has (also known as the Hamming weight).
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

def hamming_weight(n: int) -> int:
    """Counts set bits in integer using Brian Kernighan's algorithm."""
    raise NotImplementedError

