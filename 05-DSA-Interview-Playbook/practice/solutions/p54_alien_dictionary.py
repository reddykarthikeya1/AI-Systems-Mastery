"""
Problem 54: Alien Dictionary (Hard - Graphs)
There is a new alien language that uses the English alphabet. Given a list of words from the alien language dictionary sorted lexicographically by the rules of this new language, derive the order of letters in this language. If the order is invalid, return `""`.
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

def alien_order(words: list[str]) -> str:
    """Derives alien alphabet order using topological sort."""
    adj = {c: set() for w in words for c in w}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # Invalid prefix condition
            
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break
                
    visited: dict[str, bool] = {}  # False = in current DFS path, True = fully processed
    res = []
    
    def dfs(c: str) -> bool:
        if c in visited:
            return visited[c]
            
        visited[c] = False  # Mark in current recursion stack
        for nei in adj[c]:
            if not dfs(nei):
                return False
        visited[c] = True
        res.append(c)
        return True
        
    for c in list(adj.keys()):
        if c not in visited:
            if not dfs(c):
                return ""
                
    res.reverse()
    return "".join(res)


def run_tests():
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == "" # Cycle detected
    assert alien_order(["abc", "ab"]) == "" # Prefix violation
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p54_alien_dictionary!")
