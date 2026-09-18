"""Problem 05 — Course Schedule

Pattern:    Cycle detection on prerequisites
Difficulty: Medium
Target:     Time O(V + E), Space O(V + E)

``prerequisites[i] = (a, b)`` means you must take ``b`` before ``a``. Return
True if all courses can be completed.

Constraints
- ``1 <= num_courses <= 2000``

Example
    can_finish_courses(2, [(1, 0)])         -> True
    can_finish_courses(2, [(1, 0), (0, 1)]) -> False

Example:
    >>> can_finish_courses(2, [(1, 0)])
    True
    >>> can_finish_courses(2, [(1, 0), (0, 1)])
    False

Hints — read one at a time, and try again between each.

    Hint 1: 'Can I order these respecting the prerequisites?' is 'is this graph a DAG?'.
    Hint 2: So this is cycle detection, or equivalently a successful topological sort.
    Hint 3: Watch the edge direction: (a, b) means b -> a, not a -> b. Getting it backwards still detects cycles correctly here, which is why this particular bug survives - but it matters for problems that ask for the order itself.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def can_finish_courses(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    raise NotImplementedError("implement can_finish_courses")
