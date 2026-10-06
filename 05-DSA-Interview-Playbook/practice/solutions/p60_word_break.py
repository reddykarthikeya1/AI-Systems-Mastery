"""
Problem 60: Word Break (Medium - Dynamic Programming)
Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words.
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

def word_break(s: str, word_dict: list[str]) -> bool:
    """Checks if string s can be segmented into words from word_dict."""
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for w in word_dict:
            if i >= len(w) and dp[i - len(w)]:
                if s[i - len(w) : i] == w:
                    dp[i] = True
                    break
                    
    return dp[len(s)]


def run_tests():
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert word_break("", ["a"]) is True
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p60_word_break!")
