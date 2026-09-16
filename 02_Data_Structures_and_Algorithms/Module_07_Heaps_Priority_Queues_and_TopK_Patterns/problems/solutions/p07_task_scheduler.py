"""Reference solution — Problem 07: Task Scheduler With Cooldown

Pattern:    Greedy counting (heap-free)
Complexity: Time O(n), Space O(alphabet)
"""

from __future__ import annotations


def task_scheduler(tasks: list[str], n: int) -> int:
    if not tasks:
        return 0

    counts: dict[str, int] = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1

    highest = max(counts.values())
    ties = sum(1 for c in counts.values() if c == highest)

    # The most frequent task lays down (highest - 1) blocks of width (n + 1),
    # then one final row holding every task tied at that frequency.
    frame = (highest - 1) * (n + 1) + ties

    # With enough distinct tasks the frame is over-filled and there is no idle
    # time at all, so the schedule is just as long as the task list.
    return max(frame, len(tasks))
