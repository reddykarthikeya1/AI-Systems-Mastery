"""
Problem 43: Find Median from Data Stream (Hard - Heap / Priority Queue)
The median is the middle value in an ordered integer list. Design a data structure that supports adding numbers from a data stream and finding the median of all elements so far.
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

class MedianFinder:
    def __init__(self):
        raise NotImplementedError
    def add_num(self, num: int) -> None:
        raise NotImplementedError
    def find_median(self) -> float:
        raise NotImplementedError

