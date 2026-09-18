"""Problem 01 — Bleu Ngram Overlap

Topic: 09 Write Research Paper
Target: Production-grade implementation

Compute unigram clipped precision between candidate and reference tokens.

Example:
    >>> bleu_ngram_overlap(["the", "cat", "the", "cat"], ["the", "cat", "on", "the", "mat"])
    0.75

Hints:
    Hint 1: Plain precision would let a candidate spam one word to inflate
        its score artificially — BLEU's "clipping" caps how much credit a
        repeated word can earn at how many times it actually appears in the
        reference.
    Hint 2: Count word frequencies in both token lists with `Counter`, then
        for each distinct word in the candidate take `min(candidate_count,
        reference_count)`, sum those clipped counts, and divide by the
        total number of candidate tokens.
    Hint 3: A candidate word absent from the reference contributes 0 (its
        reference count is 0, not a KeyError) — use `.get(word, 0)` — and
        an empty candidate list must short-circuit to 0.0 before any
        division by `len(candidate_tokens)` occurs. Round the final ratio
        to 4 decimal places.
"""

from __future__ import annotations


def bleu_ngram_overlap(candidate_tokens: list[str], reference_tokens: list[str]) -> float:
    """Clipped unigram precision:
    sum(min(candidate_count(w), reference_count(w))) / len(candidate_tokens).
    Returns float rounded to 4 decimals (0.0 if candidate is empty).
    """
    raise NotImplementedError("Implement bleu_ngram_overlap")
