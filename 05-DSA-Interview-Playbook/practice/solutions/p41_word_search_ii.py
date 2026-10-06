"""
Problem 41: Word Search II (Hard - Tries)
Given an $m \times n$ `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from sequentially adjacent cells.
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

def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """Finds all words on board using Trie-guided backtracking DFS."""
    trie: dict = {}
    for word in words:
        curr = trie
        for ch in word:
            curr = curr.setdefault(ch, {})
        curr["$"] = word
        
    rows, cols = len(board), len(board[0])
    res = []
    
    def dfs(r: int, c: int, parent: dict):
        ch = board[r][c]
        curr_node = parent[ch]
        
        if "$" in curr_node:
            res.append(curr_node.pop("$"))
            
        board[r][c] = "#"  # Mark visited
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node:
                dfs(nr, nc, curr_node)
        board[r][c] = ch   # Backtrack
        
        # Leaf pruning optimization
        if not curr_node:
            parent.pop(ch)
            
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in trie:
                dfs(r, c, trie)
                
    return res


def run_tests():
    b = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    w = ["oath","pea","eat","rain"]
    assert sorted(find_words(b, w)) == sorted(["eat", "oath"])
    b2 = [["a","b"],["c","d"]]
    assert find_words(b2, ["abcd"]) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p41_word_search_ii!")
