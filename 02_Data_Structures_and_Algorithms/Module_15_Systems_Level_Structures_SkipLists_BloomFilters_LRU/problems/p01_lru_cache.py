"""Problem 01 — LRU Cache With O(1) Operations

Pattern:    Hash map + doubly linked list
Difficulty: Hard
Target:     Time O(1) per operation, Space O(capacity)

Simulate an LRU cache where **both** ``get`` and ``put`` are ``O(1)``.

* ``("get", key, 0)`` — return the value, or ``-1`` if absent. A hit counts as
  a use.
* ``("put", key, value)`` — insert or update. A put also counts as a use. When
  over capacity, evict the least recently used key.

Return the results of the ``get`` operations, in order.

Constraints
- ``1 <= capacity <= 3000``, ``1 <= len(ops) <= 10**5``

Example
    capacity 2, ops = [("put",1,1), ("put",2,2), ("get",1,0), ("put",3,3), ("get",2,0)]
    -> [1, -1]      (putting 3 evicted key 2, since 1 had just been used)

Hints — read one at a time, and try again between each.

    Hint 1: A dict gives O(1) lookup but no ordering. A list gives ordering but O(n) removal from the middle. You need both properties at once.
    Hint 2: A doubly linked list can unlink a known node in O(1), and a dict can map a key straight to its node. That combination is the standard answer.
    Hint 3: In Python, collections.OrderedDict already IS that combination - move_to_end and popitem(last=False) are both O(1). Implementing the linked list by hand is the real exercise; using OrderedDict is the idiomatic production answer.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def simulate_lru(capacity: int, ops: list[tuple[str, int, int]]) -> list[int]:
    raise NotImplementedError("implement simulate_lru")
