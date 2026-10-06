"""
Problem 45: Word Search (Medium - Backtracking)
Given an $m \times n$ grid of characters `board` and a string `word`, return `True` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells horizontally or vertically. The same cell may not be used more than once.
"""
from typing import List, Dict, Optional, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def exist(board: list[list[str]], word: str) -> bool:
    """Checks if word exists on board using DFS backtracking."""
    rows, cols = len(board), len(board[0])
    
    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
            
        temp = board[r][c]
        board[r][c] = "#"
        
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
                 
        board[r][c] = temp
        return found
        
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False


def run_tests():
    b = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    assert exist(b, "ABCCED") is True
    assert exist(b, "SEE") is True
    assert exist(b, "ABCB") is False
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p45_word_search!")
