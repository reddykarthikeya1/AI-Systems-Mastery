# Module 03: Linked Lists & Pointer Manipulation (0 to 100 Mastery)

> **Discontinuous Node Allocation, Pointer Chasing & In-Place Splicing**

Unlike arrays, linked lists allocate memory in discontinuous chunks on the heap. Inserting or deleting an element does not require shifting elements; it requires updating pointers. In this module, you master the core linked list patterns: **Sentinel Dummy Nodes**, **Fast & Slow Pointer Runners**, and **In-Place Three-Pointer Reversal**.

---

## 1. Physical Node Architecture vs Array Cache Locality

```
Array:        [ 0x1000 | 0x1008 | 0x1010 ]  (Contiguous -> Cache hits!)
Linked List:  [ Node A (0x7F10) ] ---> [ Node B (0x12A0) ] ---> [ Node C (0x99F0) ]
              (Discontinuous heap allocations -> CPU Cache misses!)
```

```python
class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next
```

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

### Problem 1: Reverse Linked List ([LeetCode 206](https://leetcode.com/problems/reverse-linked-list/)) — Easy

#### Brute Force: Array Value Extraction
Dump all values into a Python list, reverse the list, and write values back into the nodes.
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(N)$ extra storage.

#### Optimized: In-Place Three-Pointer Reversal
Maintain `prev = None`, `curr = head`, and `nxt = None`. At each step, point `curr.next` to `prev`, then advance `prev` and `curr`.
```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    while curr:
        nxt = curr.next     # 1. Save next node
        curr.next = prev    # 2. Reverse pointer backwards
        prev = curr         # 3. Advance prev
        curr = nxt          # 4. Advance curr
    return prev
```
- **Time Complexity**: $O(N)$ — Single pass.
- **Space Complexity**: $O(1)$ — Exactly 3 pointer variables.

---

### Problem 2: Merge Two Sorted Lists ([LeetCode 21](https://leetcode.com/problems/merge-two-sorted-lists/)) — Easy

#### Optimized: Sentinel Dummy Head Pointer Splicing
```python
def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    tail.next = list1 if list1 else list2
    return dummy.next
```
- **Time Complexity**: $O(N + M)$ — Traverses both lists once.
- **Space Complexity**: $O(1)$ — Splices existing node pointers in-place.

---

### Problem 3: Linked List Cycle ([LeetCode 141](https://leetcode.com/problems/linked-list-cycle/)) — Easy

#### Brute Force: Hash Set
Store visited node references in a hash set. If `curr in seen`, a cycle exists.
- **Time**: $O(N)$, **Space**: $O(N)$.

#### Optimized: Floyd's Tortoise and Hare ($O(1)$ Space)
Advance `slow` by 1 step and `fast` by 2 steps. If there is a cycle, the fast pointer will eventually lap the slow pointer and they will collide.
```python
def has_cycle(head: ListNode | None) -> bool:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```
- **Time Complexity**: $O(N)$ — Non-cyclic takes $N/2$ steps; cyclic takes at most $N$ steps inside cycle.
- **Space Complexity**: $O(1)$ — Only two pointers.

---

### Problem 4: Reorder List ([LeetCode 143](https://leetcode.com/problems/reorder-list/)) — Medium

#### Brute Force: Array of Nodes
Store all nodes in an array and use two pointers from front and back to relink.
- **Time**: $O(N)$, **Space**: $O(N)$.

#### Optimized: Find Middle + Reverse Second Half + Merge In-Place
1. Find middle with slow/fast pointers.
2. Reverse the second half in-place ($O(1)$ space).
3. Interleave/merge the first half and reversed second half.
```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    
    # 1. Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # 2. Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    
    # 3. Interleave two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(1)$.

---

### Problem 5: Remove Nth Node From End of List ([LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)) — Medium

#### Optimized: Fast/Slow Window with Sentinel Dummy Head
Advance `fast` $N + 1$ steps ahead from a dummy node. Then advance `slow` and `fast` simultaneously until `fast` reaches `None`. `slow.next = slow.next.next`.
```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    slow, fast = dummy, dummy
    for _ in range(n + 1):
        fast = fast.next
        
    while fast:
        slow = slow.next
        fast = fast.next
        
    slow.next = slow.next.next
    return dummy.next
```
- **Time Complexity**: $O(N)$ — Single pass.
- **Space Complexity**: $O(1)$ — In-place splicing.

---

### Problem 6: Merge K Sorted Lists ([LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/)) — Hard

#### Brute Force: Collect & Sort
Collect all values into an array, sort ($O(N \\log N)$), and build a new list.
- **Space**: $O(N)$ extra nodes.

#### Optimized: Min-Heap / Divide-and-Conquer ($O(N \\log K)$)
Push head of each of the $K$ lists into a Min-Heap. Pop smallest, link to tail, and push its `next`.
```python
import heapq

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next
```
- **Time Complexity**: $O(N \\log K)$ where $N$ is total nodes, $K$ is number of lists.
- **Space Complexity**: $O(K)$ heap memory.

---

### Problem 7: Copy List with Random Pointer ([LeetCode 138](https://leetcode.com/problems/copy-list-with-random-pointer/)) — Medium

#### Optimized: Interweaving Nodes ($O(1)$ Space)
1. Clone each node $A$ and insert $A'$ immediately after $A$: $A \\to A' \\to B \\to B'$.
2. Assign random pointers: $A'.random = A.random.next$ if $A.random$ else None.
3. Unweave the lists to restore original and extract clone.
- **Time Complexity**: $O(N)$ — Three linear passes.
- **Space Complexity**: $O(1)$ auxiliary memory (excluding cloned list).

---

### Problem 8: Reverse Nodes in k-Group ([LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/)) — Hard

#### Optimized: Iterative Group Reversal ($O(1)$ Space)
Count $k$ nodes ahead. If $k$ nodes exist, reverse the window in-place, connect with previous group's tail, and advance.
- **Time Complexity**: $O(N)$ — Each node processed twice.
- **Space Complexity**: $O(1)$ — Strict constant memory.

---

## 3. Hands-On Project & Test Suite

Verify your Doubly Linked List engine:
- Starter Template: [`starter/doubly_linked_list_engine.py`](starter/doubly_linked_list_engine.py)
- Production Solution: [`project_solution/doubly_linked_list_engine.py`](project_solution/doubly_linked_list_engine.py)
- Pytest Suite: [`project_solution/test_doubly_linked_list_engine.py`](project_solution/test_doubly_linked_list_engine.py)

## 🧪 Practice & Verification

Reading a module teaches recognition. Only the problems teach recall — and the
debug lab teaches the thing neither of them does, which is diagnosis.

### 1. Build the module project

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

Every shipped test must fail with `NotImplementedError` on an untouched
starter. If any passes, the grading loop is broken and is telling you your work
is correct when it has not been done — run `make integrity` from the course
root.

### 2. Work the problem bank — 8 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Reverse A Linked List](problems/p01_reverse_list.py) | Pointer manipulation | Easy | `Time O(n), Space O(1)` |
| 02 | [Detect A Cycle](problems/p02_has_cycle.py) | Fast and slow pointers | Easy | `Time O(n), Space O(1)` |
| 03 | [Find Where The Cycle Begins](problems/p03_cycle_start.py) | Floyd's algorithm | Medium | `Time O(n), Space O(1)` |
| 04 | [Middle Of The List](problems/p04_middle_node.py) | Fast and slow pointers | Easy | `Time O(n), Space O(1)` |
| 05 | [Merge Two Sorted Lists](problems/p05_merge_sorted.py) | Dummy head + two pointers | Easy | `Time O(n + m), Space O(1)` |
| 06 | [Remove The N-th Node From The End](problems/p06_remove_nth_from_end.py) | Dummy head + gap pointers | Medium | `Time O(n), Space O(1)` |
| 07 | [Palindrome Linked List](problems/p07_is_palindrome_list.py) | Fast/slow + in-place reversal | Medium | `Time O(n), Space O(1)` |
| 08 | [Reorder List](problems/p08_reorder_list.py) | Split + reverse + weave | Hard | `Time O(n), Space O(1)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_list_surgery.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. Reverse a list in place with three pointers, naming the order the assignments must take.
2. Explain why fast/slow pointers must move at different speeds, and where the cycle-entrance arithmetic comes from.
3. Use a dummy head to remove the 'is it the head?' special case, and name two problems where it does so.
4. Say which middle node an even-length list returns for a given loop condition, and change it deliberately.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
