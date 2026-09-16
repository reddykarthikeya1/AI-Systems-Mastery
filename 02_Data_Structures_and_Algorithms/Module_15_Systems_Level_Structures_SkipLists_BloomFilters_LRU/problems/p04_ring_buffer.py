"""Problem 04 — Fixed-Capacity Ring Buffer

Pattern:    Circular buffer
Difficulty: Medium
Target:     Time O(1) per operation, Space O(capacity)

Simulate a fixed-capacity circular buffer:

* ``("push", v)`` — append ``v``; when full, **overwrite the oldest** entry
* ``("pop", 0)`` — remove and return the oldest, or ``None`` if empty
* ``("items", 0)`` — contents oldest-first

Return the results of ``pop`` and ``items``, in order.

Constraints
- ``1 <= capacity <= 10**5``
- every operation must be O(1) — no shifting

Example
    capacity 3, ops = [("push",1),("push",2),("push",3),("push",4),("items",0)]
    -> [[2, 3, 4]]      (1 was overwritten)

Hints — read one at a time, and try again between each.

    Hint 1: A Python list with pop(0) is O(n) because everything shifts. The point of a ring buffer is that nothing ever moves.
    Hint 2: Keep a fixed-size list plus a head index and a count. Positions are computed modulo capacity.
    Hint 3: When full, a push advances the head as well as the tail - that is the overwrite. Forgetting to advance the head is the classic bug: the buffer then reports stale data as the oldest entry.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def simulate_ring_buffer(capacity: int, ops: list[tuple[str, int]]) -> list[int | None | list[int]]:
    raise NotImplementedError("implement simulate_ring_buffer")
