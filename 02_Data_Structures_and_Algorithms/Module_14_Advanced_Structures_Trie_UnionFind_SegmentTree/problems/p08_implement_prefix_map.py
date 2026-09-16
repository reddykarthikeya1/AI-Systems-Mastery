"""Problem 08 — Prefix-Sum Map: Sum Of Keys With A Prefix

Pattern:    Trie with aggregated values
Difficulty: Medium
Target:     Time O(len(key)) per operation, Space O(total characters)

Support ``("insert", key, value)`` and ``("sum", prefix, 0)``, where ``sum``
returns the total of the values of every key with that prefix. Re-inserting a
key **replaces** its value.

Return the results of the ``sum`` operations, in order.

Constraints
- ``1 <= len(ops) <= 10**4``
- lowercase keys

Example
    ops = [("insert","apple",3), ("sum","ap",0), ("insert","app",2), ("sum","ap",0)]
    -> [3, 5]

Hints — read one at a time, and try again between each.

    Hint 1: Storing the total at each trie node makes `sum` an O(len(prefix)) walk with no subtree traversal at all.
    Hint 2: On insert, add the value to every node along the key's path.
    Hint 3: Re-insertion is the trap: you must add the DELTA (new value minus old), not the new value. Adding the new value on top leaves every ancestor total permanently too high, and nothing errors.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def simulate_prefix_map(ops: list[tuple[str, str, int]]) -> list[int]:
    raise NotImplementedError("implement simulate_prefix_map")
