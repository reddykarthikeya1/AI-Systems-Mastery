"""Problem 01 — Simhash Near Duplicate Filter

Topic: 19 Distributed Web Crawler Deduplication Google
Target: Production-grade implementation

Calculate 64-bit SimHash fingerprint and compare Hamming distance to filter duplicates.

Example:
    >>> simhash_near_duplicate_filter(['distributed', 'crawler', 'python', 'systems', 'dedup'], ['distributed', 'crawler', 'python', 'systems', 'dedup'], 3)
    (True, 0)

Hints:
    Hint 1: SimHash compresses a whole document into one fixed-width
        fingerprint such that similar token sets produce fingerprints
        differing in only a few bits, turning "near-duplicate" into a
        simple bit-difference count.
    Hint 2: Per document, accumulate a 16-slot vote vector across tokens
        (each token's hash votes +1/-1 per bit depending on whether that
        bit is set), collapse the vector to a fingerprint bit (1 if the
        vote is positive), then XOR the two fingerprints and count the
        set bits for the Hamming distance.
    Hint 3: The fingerprint bit comes from the SIGN of the accumulated
        vote (`v[i] > 0`), not from any single token's raw hash bits, so
        tokens can cancel each other's votes out; use
        `bin(diff).count('1')` for the distance, and treat the duplicate
        check as `dist <= max_hamming_dist`, inclusive of the boundary.
"""

from __future__ import annotations


def simhash_near_duplicate_filter(doc1_tokens: list[str], doc2_tokens: list[str], max_hamming_dist: int = 3) -> tuple[bool, int]:
    """Compute 16-bit toy SimHash for each document:
    - 16-element accumulator vector initialized to 0
    - For each token in tokens, compute h = abs(hash(token)) & 0xFFFF
    - For each bit i (0..15): if (h & (1 << i)): v[i] += 1 else v[i] -= 1
    - fingerprint bit i = 1 if v[i] > 0 else 0
    Hamming distance = number of bits where fingerprints differ.
    Returns (is_near_duplicate, hamming_distance).
    """
    raise NotImplementedError("Implement simhash_near_duplicate_filter")
