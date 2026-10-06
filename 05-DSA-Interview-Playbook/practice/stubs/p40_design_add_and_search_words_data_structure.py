"""
Problem 40: Design Add and Search Words Data Structure (Medium - Tries)
Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can represent any letter.
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

class WordDictionary:
    def __init__(self):
        raise NotImplementedError
    def add_word(self, word: str) -> None:
        raise NotImplementedError
    def search(self, word: str) -> bool:
        raise NotImplementedError

