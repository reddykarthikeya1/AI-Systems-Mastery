"""
Problem 40: Design Add and Search Words Data Structure (Medium - Tries)
Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can represent any letter.
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

class WordNode:
    def __init__(self):
        self.children: dict[str, WordNode] = {}
        self.is_end: bool = False

class WordDictionary:
    def __init__(self):
        self.root = WordNode()

    def add_word(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = WordNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: WordNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            ch = word[idx]
            if ch != '.':
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], idx + 1)
            else:
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
        return dfs(self.root, 0)


def run_tests():
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True
    assert wd.search("...") is True and wd.search("....") is False        # length must match
    assert wd.search("b.d") is True and wd.search("b.e") is False
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p40_design_add_and_search_words_data_structure!")
