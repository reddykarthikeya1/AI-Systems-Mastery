"""Problem 06 — Min Stack (O(1) Minimum)

Pattern:    Stack with auxiliary state
Difficulty: Medium
Target:     Time O(1) per operation, Space O(n)

Simulate a stack supporting ``push``, ``pop``, ``top`` and ``get_min``, where
**every operation is O(1)** — including ``get_min``.

``ops`` is a list of ``(name, argument)`` pairs. ``push`` carries an int; the
others carry ``None``. Return the list of results produced by ``top`` and
``get_min`` (``push`` and ``pop`` produce nothing). Return ``None`` for ``top``
or ``get_min`` on an empty stack.

Constraints
- ``1 <= len(ops) <= 10**5``

Example
    ops = [("push", 3), ("push", 1), ("get_min", None), ("pop", None), ("get_min", None)]
    -> [1, 3]

Hints — read one at a time, and try again between each.

    Hint 1: Scanning the stack for the minimum is O(n). You need the minimum available without looking.
    Hint 2: Keep a second stack holding the minimum *as of* each push.
    Hint 3: Push min(new_value, current_min) onto it every time, and pop both stacks together. Then the min stack's top is always the current minimum, and pop stays O(1).

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def simulate_min_stack(ops: list[tuple[str, int | None]]) -> list[int | None]:
    raise NotImplementedError("implement simulate_min_stack")
