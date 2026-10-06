"""
Problem 7: Encode and Decode Strings (Medium - Arrays & Hashing)
Design an algorithm to encode a list of strings to a single string, and decode that string back to the original list of strings. The strings can contain any possible characters, including delimiters like '#' and commas.
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

class Codec:
    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string."""
        res = []
        for s in strs:
            res.append(f"{len(s)}#{s}")
        return "".join(res)

    def decode(self, s: str) -> list[str]:
        """Decodes a single string to a list of strings."""
        res = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            length = int(s[i:j])
            word = s[j + 1 : j + 1 + length]
            res.append(word)
            i = j + 1 + length
        return res


def run_tests():
    c = Codec()
    assert c.decode(c.encode(["lint", "code", "love", "you"])) == ["lint", "code", "love", "you"]
    assert c.decode(c.encode(["#", "##", "3#cat"])) == ["#", "##", "3#cat"]
    assert c.decode(c.encode(["", ""])) == ["", ""]
    assert c.decode(c.encode([])) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p07_encode_and_decode_strings!")
