"""Problem 03 — Skip List: Insert, Search, Delete

Pattern:    Skip list
Difficulty: Hard
Target:     Expected O(log n) per operation, Space O(n)

Simulate a sorted set backed by a skip list, supporting:

* ``("insert", v)`` — add ``v`` (idempotent); returns nothing
* ``("search", v)`` — is ``v`` present?
* ``("delete", v)`` — remove ``v``; returns whether it was there
* ``("items", 0)`` — the sorted contents as a list

Return the results of ``search``, ``delete`` and ``items``, in order.

Constraints
- ``1 <= len(ops) <= 10**4``
- expected O(log n) per operation

Example
    ops = [("insert",3), ("insert",1), ("search",3), ("items",0), ("delete",3), ("search",3)]
    -> [True, [1, 3], True, False]

Hints — read one at a time, and try again between each.

    Hint 1: A skip list is a stack of linked lists. The bottom level holds every element; each level above holds a random subset of the level below.
    Hint 2: Search walks forward at the top level while the next value is smaller, then drops a level and repeats. That is what gives O(log n) expected.
    Hint 3: Use a FIXED random seed so the structure is reproducible - a randomised structure with a test suite needs deterministic behaviour or failures cannot be replayed.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def simulate_skip_list(ops: list[tuple[str, int]]) -> list[bool | list[int]]:
    raise NotImplementedError("implement simulate_skip_list")
