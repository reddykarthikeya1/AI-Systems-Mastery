# DSA Core 75: Practice Workbook

> Every problem has a stub to complete, a reference solution kept closed, hidden asserts, and (for 70 problems) a randomised cross-check against a brute-force oracle. The statements below come straight from the problem files.

## The loop for every problem

```text
python practice/run_tests.py 12 --hint 12        # a hint (repeat for levels 1, 2, 3)
python practice/run_tests.py 12 --stub           # test YOUR stubs/p12_*.py: asserts plus random cross-check
python practice/trace.py 12 "[0,1,0,2,1,0,1,3,2,1,2,1]" --stub   # dry-run trace of your code on an input
python practice/run_tests.py 12                  # the reference solution, once you are done
```

**75 problems in 14 categories.**

---

## Arrays & Hashing

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 1 | Two Sum | Easy | Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you may not use the same element twice. |
| 2 | Contains Duplicate | Easy | Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct. |
| 3 | Valid Anagram | Easy | Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise. |
| 4 | Group Anagrams | Medium | Given an array of strings `strs`, group the anagrams together. You can return the answer in any order. |
| 5 | Top K Frequent Elements | Medium | Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order. |
| 6 | Product of Array Except Self | Medium | Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Must run in $O(N)$ time without using division. |
| 7 | Encode and Decode Strings | Medium | Design an algorithm to encode a list of strings to a single string, and decode that string back to the original list of strings. The strings can contain any possible characters, including delimiters like '#' and commas. |
| 8 | Longest Consecutive Sequence | Medium | Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time. |

## Two Pointers

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 9 | Valid Palindrome | Easy | A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. |
| 10 | 3Sum | Medium | Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets. |
| 11 | Container With Most Water | Medium | You are given an integer array `height` of length $n$. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store. |
| 12 | Trapping Rain Water | Hard | Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining. |

## Sliding Window

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 13 | Best Time to Buy and Sell Stock | Easy | You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\text{th}}$ day. Maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that... |
| 14 | Longest Substring Without Repeating Characters | Medium | Given a string `s`, find the length of the longest substring without duplicate characters. |
| 15 | Longest Repeating Character Replacement | Medium | You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times. Return the length of the longest substring containing the same... |
| 16 | Minimum Window Substring | Hard | Given two strings `s` and `t` of lengths $m$ and $n$ respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists,... |

## Stack

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 17 | Valid Parentheses | Easy | Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid. |
| 18 | Daily Temperatures | Medium | Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the $i^{\text{th}}$ day to get a warmer temperature. If... |
| 19 | Largest Rectangle in Histogram | Hard | Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram. |

## Binary Search

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 20 | Binary Search | Easy | Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`. |
| 21 | Search in Rotated Sorted Array | Medium | There is an integer array `nums` sorted in ascending order (with distinct values), rotated at an unknown pivot index. Given `nums` and a `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`. |
| 22 | Find Minimum in Rotated Sorted Array | Medium | Suppose an array of length $n$ sorted in ascending order is rotated between 1 and $n$ times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array. Must run in $O(\log N)$ time. |

## Linked List

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 23 | Reverse Linked List | Easy | Given the `head` of a singly linked list, reverse the list, and return the reversed list. |
| 24 | Merge Two Sorted Lists | Easy | You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list by splicing together the nodes of the first two lists. Return the head of the merged linked list. |
| 25 | Reorder List | Medium | You are given the head of a singly linked-list: $L_0 \to L_1 \to \dots \to L_{n - 1} \to L_n$. Reorder the list to: $L_0 \to L_n \to L_1 \to L_{n - 1} \to L_2 \to L_{n - 2} \dots$ in-place without modifying node values. |
| 26 | Remove Nth Node From End of List | Medium | Given the `head` of a linked list, remove the $n^{\text{th}}$ node from the end of the list and return its head in one single pass. |
| 27 | Linked List Cycle | Easy | Given `head`, the head of a linked list, determine if the linked list has a cycle in it using $O(1)$ memory. |
| 28 | Merge K Sorted Lists | Hard | You are given an array of $k$ linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it. |

## Trees

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 29 | Invert Binary Tree | Easy | Given the `root` of a binary tree, invert the tree (mirror reflection), and return its root. |
| 30 | Maximum Depth of Binary Tree | Easy | Given the `root` of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf). |
| 31 | Same Tree | Easy | Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same value. |
| 32 | Subtree of Another Tree | Easy | Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise. |
| 33 | Lowest Common Ancestor of a BST | Medium | Given a Binary Search Tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST. |
| 34 | Binary Tree Level Order Traversal | Medium | Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level). |
| 35 | Validate Binary Search Tree | Medium | Given the `root` of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values to be strictly less than node value, and all right subtree values strictly greater. |
| 36 | Kth Smallest Element in a BST | Medium | Given the `root` of a binary search tree, and an integer `k`, return the $k^{\text{th}}$ smallest value (1-indexed) of all the values of the nodes in the tree. |
| 37 | Construct Binary Tree from Preorder and Inorder Traversal | Medium | Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree. |
| 38 | Binary Tree Maximum Path Sum | Hard | A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path. |

## Tries

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 39 | Implement Trie (Prefix Tree) | Medium | A trie (pronounced 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement `insert`, `search`, and `starts_with` methods. |
| 40 | Design Add and Search Words Data Structure | Medium | Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can represent any letter. |
| 41 | Word Search II | Hard | Given an $m \times n$ `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from sequentially adjacent cells. |

## Heap / Priority Queue

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 42 | Kth Largest Element in an Array | Medium | Given an integer array `nums` and an integer `k`, return the $k^{\text{th}}$ largest element in the array. Note that it is the $k^{\text{th}}$ largest element in sorted order, not the $k^{\text{th}}$ distinct element. |
| 43 | Find Median from Data Stream | Hard | The median is the middle value in an ordered integer list. Design a data structure that supports adding numbers from a data stream and finding the median of all elements so far. |

## Backtracking

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 44 | Combination Sum | Medium | Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen unlimited times. |
| 45 | Word Search | Medium | Given an $m \times n$ grid of characters `board` and a string `word`, return `True` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells horizontally or vertically. The same cell may not... |
| 46 | Subsets | Medium | Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order. |

## Graphs

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 47 | Number of Islands | Medium | Given an $m \times n$ 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or... |
| 48 | Clone Graph | Medium | Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors. |
| 49 | Pacific Atlantic Water Flow | Medium | There is an $m \times n$ rectangular island that borders both the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges). Water flows from a cell to an adjacent cell with an equal or lower height.... |
| 50 | Course Schedule | Medium | There are a total of `numCourses` courses you have to take, labeled from $0$ to $\text{numCourses} - 1$. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course $b$ first if... |
| 51 | Number of Connected Components in an Undirected Graph | Medium | You have a graph of $n$ nodes. You are given an integer $n$ and an array `edges` where `edges[i] = [a, b]` indicates that there is an edge between $a$ and $b$ in the graph. Return the number of connected components in the graph. |
| 52 | Graph Valid Tree | Medium | Given $n$ nodes labeled from $0$ to $n - 1$ and a list of undirected edges, write a function to check whether these edges make up a valid tree. |
| 53 | Network Delay Time | Medium | You are given a network of $n$ nodes, labeled from $1$ to $n$. You are also given `times`, a list of travel times as directed edges `times[i] = (u, v, w)`. We will send a signal from node $k$. Return the minimum time it takes... |
| 54 | Alien Dictionary | Hard | There is a new alien language that uses the English alphabet. Given a list of words from the alien language dictionary sorted lexicographically by the rules of this new language, derive the order of letters in this language.... |

## Dynamic Programming

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 55 | Climbing Stairs | Easy | You are climbing a staircase. It takes $n$ steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top? |
| 56 | House Robber | Medium | You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent... |
| 57 | House Robber II | Medium | You are a professional robber planning to rob houses along a street, but all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Determine the maximum amount of money you... |
| 58 | Coin Change | Medium | You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that... |
| 59 | Longest Increasing Subsequence | Medium | Given an integer array `nums`, return the length of the longest strictly increasing subsequence. |
| 60 | Word Break | Medium | Given a string `s` and a dictionary of strings `wordDict`, return `True` if `s` can be segmented into a space-separated sequence of one or more dictionary words. |
| 61 | Combination Sum IV | Medium | Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations (permutations) that add up to `target`. |
| 62 | Decode Ways | Medium | A message containing letters from A-Z can be encoded into numbers using the mapping `'A' -> 1, 'B' -> 2, ... 'Z' -> 26`. Given a string `s` containing only digits, return the number of ways to decode it. |
| 63 | Unique Paths | Medium | There is a robot on an $m \times n$ grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Return the number... |
| 64 | Longest Common Subsequence | Medium | Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`. |
| 65 | Edit Distance | Medium | Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You have three operations permitted on a word: insert a character, delete a character, or replace a character. |
| 66 | Partition Equal Subset Sum | Medium | Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise. |
| 67 | Jump Game | Medium | You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `True` if you can reach the last index,... |

## Intervals

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 68 | Insert Interval | Medium | You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval`. Insert `newInterval` into... |
| 69 | Merge Intervals | Medium | Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input. |
| 70 | Non-overlapping Intervals | Medium | Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping. |
| 71 | Meeting Rooms | Easy | Given an array of meeting time intervals where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings without overlap. |
| 72 | Meeting Rooms II | Medium | Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required. |

## Bit Manipulation

| # | Problem | Level | Statement |
| :-: | :--- | :-: | :--- |
| 73 | Number of 1 Bits | Easy | Given a positive integer `n`, write a function that returns the number of set bits (1s) it has (also known as the Hamming weight). |
| 74 | Counting Bits | Easy | Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of 1's in the binary representation of `i`. Must run in $O(N)$ linear time. |
| 75 | Missing Number | Easy | Given an array `nums` containing $n$ distinct numbers in the range $[0, n]$, return the only number in the range that is missing from the array. |

