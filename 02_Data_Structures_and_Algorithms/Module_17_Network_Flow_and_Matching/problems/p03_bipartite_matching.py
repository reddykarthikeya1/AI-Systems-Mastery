"""Problem 03 - Maximum Bipartite Matching

Pattern:    Unit-capacity flow
Difficulty: Medium
Target:     Time O(E * sqrt(V))

``left`` workers, ``right`` jobs, and a list of ``(worker, job)``
pairs meaning that worker can do that job. Assign at most one job per worker and
at most one worker per job. Return the size of the largest assignment.

Constraints
- ``1 <= left, right <= 200``, ``0 <= len(pairs) <= 10**4``

Example
    max_matching(2, 2, [(0,0),(0,1),(1,0)]) -> 2

Greedy gets this wrong: taking ``(0,0)`` first strands worker 1. The answer is
2, by giving job 1 to worker 0 and job 0 to worker 1.

Example:
    >>> max_matching(2, 2, [(0, 0), (0, 1), (1, 0)])
    2

Hints - read one at a time, and try again between each.

    Hint 1: Super-source -> every worker, every job -> super-sink, all with capacity 1. Keep the qualification edges at capacity 1 too.
    Hint 2: One unit of flow is one assignment. The capacity-1 edge out of the source is what stops a worker being given two jobs.
    Hint 3: The answer is just the value of the max flow. You do not need to extract the assignment for this problem.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def max_matching(left: int, right: int,
                 pairs: list[tuple[int, int]]) -> int:
    raise NotImplementedError("implement max_matching")
