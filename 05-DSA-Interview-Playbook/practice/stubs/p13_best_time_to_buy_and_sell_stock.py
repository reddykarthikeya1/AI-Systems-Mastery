"""
Problem 13: Best Time to Buy and Sell Stock (Easy - Sliding Window)
You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\text{th}}$ day. Maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
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

def max_profit(prices: list[int]) -> int:
    """Calculates maximum profit from a single buy and sell transaction.
    
    Time: O(N), Space: O(1)
    """
    raise NotImplementedError

