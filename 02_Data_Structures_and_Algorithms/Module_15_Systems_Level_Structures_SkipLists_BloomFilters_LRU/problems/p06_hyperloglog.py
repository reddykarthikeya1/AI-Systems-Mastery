"""Problem 06 — Approximate Distinct Count

Pattern:    Probabilistic cardinality estimation
Difficulty: Hard
Target:     Time O(n), Space O(registers)

Estimate the number of **distinct** strings in ``items`` using
``registers`` counters and no per-item storage.

Constraints
- ``0 <= len(items) <= 10**6``
- ``registers`` is a power of two
- must be deterministic
- the estimate must land within ±15% of the true count for counts above 1000

Example
    approx_distinct(["a"] * 1000 + ["b"] * 1000) -> approximately 2

An exact `set` costs O(distinct) memory. HyperLogLog costs a fixed few
kilobytes regardless of cardinality — which is why Redis uses it to count
unique visitors instead of storing them.

Hints — read one at a time, and try again between each.

    Hint 1: The core observation: in a stream of uniformly random hashes, seeing a hash with k leading zeros suggests roughly 2^k distinct values.
    Hint 2: One such estimate is extremely noisy. So split the hash: use the first bits to pick a register, and record the maximum leading-zero count seen in each register.
    Hint 3: Combine the registers with the harmonic mean and multiply by the standard bias-correction constant alpha * m^2. Use hashlib rather than hash() so the result is reproducible.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def approx_distinct(items: list[str], registers: int = 1024) -> int:
    raise NotImplementedError("implement approx_distinct")
