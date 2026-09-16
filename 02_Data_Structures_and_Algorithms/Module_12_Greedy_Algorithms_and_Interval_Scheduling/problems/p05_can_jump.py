"""Problem 05 — Jump Game

Pattern:    Greedy reachability
Difficulty: Medium
Target:     Time O(n), Space O(1)

``nums[i]`` is the maximum jump length from index ``i``. Starting at index 0,
return True if the last index is reachable.

Constraints
- ``1 <= len(nums) <= 10**4``  -> O(n) expected

Example
    can_jump([2, 3, 1, 1, 4]) -> True
    can_jump([3, 2, 1, 0, 4]) -> False

Hints — read one at a time, and try again between each.

    Hint 1: You do not need to know WHICH jumps to take, only how far you can possibly get.
    Hint 2: Sweep left to right keeping the furthest reachable index.
    Hint 3: If you ever stand on an index beyond that reach, you are stuck. Otherwise extend the reach with i + nums[i].

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def can_jump(nums: list[int]) -> bool:
    raise NotImplementedError("implement can_jump")
