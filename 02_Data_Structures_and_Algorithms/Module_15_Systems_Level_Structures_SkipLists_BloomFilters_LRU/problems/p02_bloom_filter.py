"""Problem 02 — Bloom Filter: No False Negatives

Pattern:    Bloom filter
Difficulty: Hard
Target:     Time O((n + q) * hashes), Space O(bits)

Insert every string in ``items`` into a Bloom filter of ``bits`` bits using
``hashes`` hash functions, then return the membership verdict for each query.

The contract, and it is asymmetric:

* **No false negatives.** Anything inserted must report True. Always.
* **False positives are allowed.** Something never inserted may report True.

Constraints
- ``0 <= len(items) <= 10**4``
- must be deterministic — the same input gives the same answers every run

Example
    bloom_check(["cat"], ["cat", "dog"]) -> [True, ...]
    where the first entry is guaranteed True and the second is usually False.

Example:
    >>> bloom_check(["cat"], ["cat", "dog"])
    [True, False]

Hints — read one at a time, and try again between each.

    Hint 1: Set `hashes` bits per item, and report True only when ALL of a query's bits are set.
    Hint 2: That is why there are no false negatives: an inserted item's bits are set and never cleared, so its check cannot fail.
    Hint 3: Derive several independent hashes deterministically from one - hashlib.md5 of the item plus a salt index works and is stable across runs, whereas Python's built-in hash() is randomised per process and would break reproducibility.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def bloom_check(items: list[str], queries: list[str], bits: int = 8192, hashes: int = 3) -> list[bool]:
    raise NotImplementedError("implement bloom_check")
