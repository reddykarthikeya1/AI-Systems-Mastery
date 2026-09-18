"""Problem 07 — Task Scheduler With Cooldown

Pattern:    Greedy counting (heap-free)
Difficulty: Medium
Target:     Time O(n), Space O(alphabet)

Each task takes one unit of time. Two identical tasks must be separated by at
least ``n`` units, during which the CPU may run a different task or idle.
Return the minimum total time to finish everything.

Constraints
- ``1 <= len(tasks) <= 10**4``
- ``0 <= n <= 100``

Example
    task_scheduler(["A","A","A","B","B","B"], 2) -> 8    (A B _ A B _ A B)
    task_scheduler(["A","A","A","B","B","B"], 0) -> 6

Example:
    >>> task_scheduler(["A", "A", "A", "B", "B", "B"], 2)
    8
    >>> task_scheduler(["A", "A", "A", "B", "B", "B"], 0)
    6

Hints — read one at a time, and try again between each.

    Hint 1: A heap simulation works, but there is a closed form. Think about the most frequent task.
    Hint 2: If the most frequent task occurs f times, it creates f-1 gaps of length n between its own runs. Those gaps get filled by other tasks or idling.
    Hint 3: Frame: (f - 1) * (n + 1) + (number of tasks tied at frequency f). The answer is max(frame, len(tasks)) - when there are many distinct tasks there is no idling at all and the length is simply the task count.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def task_scheduler(tasks: list[str], n: int) -> int:
    raise NotImplementedError("implement task_scheduler")
