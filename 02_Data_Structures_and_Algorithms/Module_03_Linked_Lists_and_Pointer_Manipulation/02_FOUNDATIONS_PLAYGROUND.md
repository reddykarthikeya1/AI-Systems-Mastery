# 🐣 Interactive Foundations Playground: Linked Lists & Pointer Manipulation

> *"A linked list is a treasure hunt: each clue only tells you where to find the next clue."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from dataclasses import dataclass
from typing import Optional
```

---

## 1. Node Definition and Pointer Traversal

A singly-linked node packages a payload value and a reference pointer to the successor node or `None`.

```python
@dataclass
class Node:
    val: int
    next: Optional['Node'] = None

head = Node(1, Node(2, Node(3)))
vals = []
curr = head
while curr:
    vals.append(curr.val)
    curr = curr.next

assert vals == [1, 2, 3]
assert head.next.val == 2
print(f"Traversed linked list: {vals}")
```

---

## 2. Three-Pointer In-Place Reversal

Reversing pointers without allocating new nodes requires tracking three consecutive pointers: `prev`, `curr`, and `next_node`.

```python
prev = None
curr = head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt

new_head = prev
reversed_vals = []
curr = new_head
while curr:
    reversed_vals.append(curr.val)
    curr = curr.next

assert reversed_vals == [3, 2, 1]
assert new_head.val == 3
print(f"Reversed list: {reversed_vals}")
```

---

## 3. Floyd's Tortoise and Hare Cycle Invariant

If a cycle exists in a linked list, a pointer moving at 2 steps per turn will always catch up to a pointer moving at 1 step per turn inside the cycle.

```python
n1, n2, n3 = Node(10), Node(20), Node(30)
n1.next = n2
n2.next = n3
n3.next = n2  # cycle back to n2

slow, fast = n1, n1
has_cycle = False
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        has_cycle = True
        break

assert has_cycle is True, "Cycle must be detected"
assert slow.val == 20 or slow.val == 30
print(f"Cycle detected successfully inside loop at node with val={slow.val}")
```

---
