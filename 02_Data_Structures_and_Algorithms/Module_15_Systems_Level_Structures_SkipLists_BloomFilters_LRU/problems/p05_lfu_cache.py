"""Problem 05 — LFU Cache

Pattern:    Frequency buckets
Difficulty: Hard
Target:     Time O(1) per operation, Space O(capacity)

Least-Frequently-Used eviction. On overflow, evict the least frequently used
key; break ties by evicting the least recently used among them.

* ``("get", key, 0)`` — the value or ``-1``; a hit increments the frequency
* ``("put", key, value)`` — insert or update; both count as a use

Return the ``get`` results, in order.

Constraints
- ``1 <= capacity <= 10**4``, ``1 <= len(ops) <= 10**5``
- O(1) per operation is the target

Example
    capacity 2, ops = [("put",1,1),("put",2,2),("get",1,0),("put",3,3),("get",2,0),("get",3,0)]
    -> [1, -1, 3]

Hints — read one at a time, and try again between each.

    Hint 1: LFU needs more state than LRU: a value per key, a frequency per key, and an ordering within each frequency.
    Hint 2: Keep a dict from frequency to an OrderedDict of the keys at that frequency. Then the eviction candidate is the first key in the bucket for the minimum frequency.
    Hint 3: Maintain `min_freq` incrementally. On a use, the key moves from bucket f to f+1; if bucket f empties and f was the minimum, the minimum becomes f+1. That is what keeps eviction O(1) instead of a scan.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def simulate_lfu(capacity: int, ops: list[tuple[str, int, int]]) -> list[int]:
    raise NotImplementedError("implement simulate_lfu")
