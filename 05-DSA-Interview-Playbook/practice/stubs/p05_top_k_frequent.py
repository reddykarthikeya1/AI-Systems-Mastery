"""
Problem 5: Top K Frequent Elements (Medium - Arrays & Hashing)
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.
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

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Returns the k most frequent elements using bucket sort.
    
    Time: O(N), Space: O(N)
    """
    raise NotImplementedError

