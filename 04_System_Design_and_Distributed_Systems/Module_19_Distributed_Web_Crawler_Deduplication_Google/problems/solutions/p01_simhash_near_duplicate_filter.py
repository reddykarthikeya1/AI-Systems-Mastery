"""Reference Solution — Problem 01: Simhash Near Duplicate Filter

Topic: 19 Distributed Web Crawler Deduplication Google
"""

from __future__ import annotations


def simhash_near_duplicate_filter(doc1_tokens: list[str], doc2_tokens: list[str], max_hamming_dist: int = 3) -> tuple[bool, int]:
    def simhash(tokens: list[str]) -> int:
        v = [0] * 16
        for t in tokens:
            h = abs(hash(t)) & 0xFFFF
            for i in range(16):
                if h & (1 << i):
                    v[i] += 1
                else:
                    v[i] -= 1
        fp = 0
        for i in range(16):
            if v[i] > 0:
                fp |= (1 << i)
        return fp

    fp1 = simhash(doc1_tokens)
    fp2 = simhash(doc2_tokens)
    diff = fp1 ^ fp2
    dist = bin(diff).count('1')
    return (dist <= max_hamming_dist, dist)
