"""Problem 08 — Consistent Hashing Ring

Pattern:    Consistent hashing
Difficulty: Hard
Target:     Time O((n*v) log(n*v) + k log(n*v)), Space O(n*v)

Build a consistent-hash ring over ``nodes`` using ``vnodes`` virtual nodes
each, assign every key to a node, then add ``new_node`` and return the
**fraction of keys that moved**.

With naive ``hash(key) % n`` this fraction approaches 1 when ``n`` changes. With
consistent hashing it should be close to ``1 / (n + 1)``.

Constraints
- ``1 <= len(nodes) <= 100``
- ``1 <= len(keys) <= 10**5``
- must be deterministic

Example
    3 nodes, 10000 keys, adding a 4th -> approximately 0.25, not ~1.0

Example:
    >>> keys = [f"key{i}" for i in range(10000)]
    >>> round(remap_fraction(["n1", "n2", "n3"], "n4", keys), 2)
    0.24

Hints — read one at a time, and try again between each.

    Hint 1: Hash each node several times (the virtual nodes) onto a numeric ring, and keep the ring sorted.
    Hint 2: A key belongs to the first virtual node clockwise from its own hash - which is a binary search, wrapping to index 0 past the end.
    Hint 3: Virtual nodes are what make the distribution even. With one point per node the load is badly skewed, which is the whole reason the parameter defaults to 150.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def remap_fraction(nodes: list[str], new_node: str, keys: list[str], vnodes: int = 150) -> float:
    raise NotImplementedError("implement remap_fraction")
