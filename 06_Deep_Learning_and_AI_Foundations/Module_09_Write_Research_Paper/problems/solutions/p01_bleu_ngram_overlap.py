"""Reference Solution — Problem 01: Bleu Ngram Overlap

Topic: 09 Write Research Paper
"""

from __future__ import annotations


def bleu_ngram_overlap(candidate_tokens: list[str], reference_tokens: list[str]) -> float:
    from collections import Counter
    if not candidate_tokens:
        return 0.0
    c_counts = Counter(candidate_tokens)
    r_counts = Counter(reference_tokens)
    clipped = sum(min(c_counts[w], r_counts.get(w, 0)) for w in c_counts)
    return round(clipped / len(candidate_tokens), 4)
