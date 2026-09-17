"""Problem 01 — Bleu Ngram Overlap

Topic: 09 Write Research Paper
Target: Production-grade implementation

Compute unigram clipped precision between candidate and reference tokens.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bleu_ngram_overlap(candidate_tokens: list[str], reference_tokens: list[str]) -> float:
    """Clipped unigram precision:
    sum(min(candidate_count(w), reference_count(w))) / len(candidate_tokens).
    Returns float rounded to 4 decimals (0.0 if candidate is empty).
    """
    raise NotImplementedError("Implement bleu_ngram_overlap")
